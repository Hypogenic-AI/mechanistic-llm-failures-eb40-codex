import json
import os
import random
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
from datasets import load_from_disk
from openai import OpenAI
from scipy import stats
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


@dataclass
class Config:
    seed: int = 42
    api_model: str = "gpt-4.1"
    judge_model: str = "gpt-4.1"
    local_model: str = "distilgpt2"
    sample_size: int = 120
    judge_subset: int = 80
    max_tokens_direct: int = 16
    max_tokens_cot: int = 200
    max_tokens_judge: int = 120
    temperature: float = 0.0


def ensure_dirs() -> None:
    for d in ["results", "results/plots", "results/model_outputs", "logs"]:
        Path(d).mkdir(parents=True, exist_ok=True)


def load_csqa_subset(sample_size: int, seed: int) -> List[dict]:
    ds = load_from_disk("datasets/commonsense_qa")["validation"]
    idx = list(range(len(ds)))
    rng = random.Random(seed)
    rng.shuffle(idx)
    subset = [ds[i] for i in idx[:sample_size]]
    return subset


def format_question(example: dict) -> str:
    q = example["question"].strip()
    labels = example["choices"]["label"]
    texts = example["choices"]["text"]
    choices = "\n".join([f"{l}. {t}" for l, t in zip(labels, texts)])
    return f"Question: {q}\nOptions:\n{choices}\n"


def parse_answer(text: str, condition: str) -> str:
    text_up = text.upper()
    if condition == "cot":
        m = re.search(r"FINAL_ANSWER\s*[:\-]\s*([A-E])\b", text_up)
        if m:
            return m.group(1)
    else:
        m = re.match(r"^\s*([A-E])\s*$", text_up)
        if m:
            return m.group(1)

    # Fallback: use the last explicit option letter mention.
    all_letters = re.findall(r"\b([A-E])\b", text_up)
    return all_letters[-1] if all_letters else ""


def get_client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for this experiment.")
    return OpenAI(api_key=key)


def chat_completion(client: OpenAI, model: str, messages: List[dict], max_tokens: int, temperature: float) -> str:
    for attempt in range(5):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message.content or ""
        except Exception:
            sleep_s = min(2 ** attempt, 20)
            time.sleep(sleep_s)
    return ""


def run_behavioral_eval(config: Config, data: List[dict], cache_path: Path) -> pd.DataFrame:
    client = get_client()
    cache: Dict[str, dict] = {}
    if cache_path.exists():
        with cache_path.open() as f:
            for line in f:
                row = json.loads(line)
                cache[row["cache_key"]] = row

    out_rows = []
    for ex in tqdm(data, desc="API eval"):
        qtxt = format_question(ex)
        ex_id = ex["id"]
        gold = ex["answerKey"]
        option_map = dict(zip(ex["choices"]["label"], ex["choices"]["text"]))

        for condition in ["direct", "cot"]:
            cache_key = f"{condition}::{ex_id}"
            if cache_key in cache:
                row = cache[cache_key]
                out_rows.append(row)
                continue

            if condition == "direct":
                messages = [
                    {"role": "system", "content": "You answer multiple-choice questions. Output exactly one letter from A to E."},
                    {"role": "user", "content": qtxt + "\nReturn only the best option letter."},
                ]
                max_tokens = config.max_tokens_direct
            else:
                messages = [
                    {"role": "system", "content": "You reason carefully and solve commonsense multiple-choice tasks."},
                    {"role": "user", "content": qtxt + "\nThink step-by-step briefly, then end with: FINAL_ANSWER: <A-E>"},
                ]
                max_tokens = config.max_tokens_cot

            raw = chat_completion(client, config.api_model, messages, max_tokens=max_tokens, temperature=config.temperature)
            pred = parse_answer(raw, condition)
            row = {
                "cache_key": cache_key,
                "id": ex_id,
                "condition": condition,
                "question": ex["question"],
                "question_with_options": qtxt,
                "options_json": json.dumps(option_map),
                "gold": gold,
                "prediction": pred,
                "prediction_text": option_map.get(pred, ""),
                "correct": int(pred == gold),
                "raw_output": raw,
            }
            out_rows.append(row)
            with cache_path.open("a") as f:
                f.write(json.dumps(row) + "\n")

    return pd.DataFrame(out_rows)


def run_coherence_judging(config: Config, results_df: pd.DataFrame, cache_path: Path) -> pd.DataFrame:
    client = get_client()
    cache: Dict[str, dict] = {}
    if cache_path.exists():
        with cache_path.open() as f:
            for line in f:
                row = json.loads(line)
                cache[row["cache_key"]] = row

    unique_ids = results_df["id"].unique().tolist()
    random.Random(config.seed).shuffle(unique_ids)
    judge_ids = set(unique_ids[: min(config.judge_subset, len(unique_ids))])

    judged_rows = []
    candidate_df = results_df[results_df["id"].isin(judge_ids)]

    for _, row in tqdm(candidate_df.iterrows(), total=len(candidate_df), desc="Coherence judging"):
        cache_key = f"judge::{row['condition']}::{row['id']}"
        if cache_key in cache:
            judged_rows.append(cache[cache_key])
            continue

        options_json = row.get("options_json", "{}")
        try:
            option_map = json.loads(options_json)
        except Exception:
            option_map = {}
        pred_text = option_map.get(row["prediction"], "")

        prompt = (
            "Assess whether the chosen option is coherent with the likely goal in the question.\n"
            "Return JSON only: {\"coherent\":0_or_1,\"reason\":\"<=20 words\"}.\n\n"
            f"{row.get('question_with_options', 'Question: ' + row['question'])}\n"
            f"Chosen option letter: {row['prediction']}\n"
            f"Chosen option text: {pred_text}\n"
            "If the chosen option is missing/invalid, coherent must be 0."
        )
        messages = [
            {"role": "system", "content": "You are a strict commonsense coherence judge."},
            {"role": "user", "content": prompt},
        ]
        raw = chat_completion(client, config.judge_model, messages, max_tokens=config.max_tokens_judge, temperature=0.0)

        coherent = 0
        reason = "parse_failed"
        try:
            payload = json.loads(raw)
            coherent = int(payload.get("coherent", 0))
            reason = str(payload.get("reason", ""))
        except Exception:
            m = re.search(r"\b([01])\b", raw)
            if m:
                coherent = int(m.group(1))
            reason = raw[:60]

        judged = {
            "cache_key": cache_key,
            "id": row["id"],
            "condition": row["condition"],
            "correct": int(row["correct"]),
            "coherent": coherent,
            "reason": reason,
            "raw_judge": raw,
        }
        judged_rows.append(judged)
        with cache_path.open("a") as f:
            f.write(json.dumps(judged) + "\n")

    return pd.DataFrame(judged_rows)


def mcnemar_exact(direct_correct: np.ndarray, cot_correct: np.ndarray) -> dict:
    # b: direct correct / cot wrong, c: direct wrong / cot correct
    b = int(np.sum((direct_correct == 1) & (cot_correct == 0)))
    c = int(np.sum((direct_correct == 0) & (cot_correct == 1)))
    n = b + c
    p = 1.0 if n == 0 else stats.binomtest(min(b, c), n=n, p=0.5, alternative="two-sided").pvalue
    return {"b": b, "c": c, "n_discordant": n, "p_value": p}


def build_local_prompt(example: dict) -> str:
    return format_question(example) + "Answer:"


def prepare_local_model(name: str):
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
    return tok, model, device


def option_logits(tok, model, device, prompt: str, layer_ablate: int = -1) -> Dict[str, float]:
    inputs = tok(prompt, return_tensors="pt").to(device)

    handle = None
    if layer_ablate >= 0:
        layer_mod = model.transformer.h[layer_ablate]

        def hook_fn(module, inp, out):
            if isinstance(out, tuple):
                hs = out[0].clone()
                hs[:, -1, :] = 0.0
                return (hs,) + out[1:]
            hs = out.clone()
            hs[:, -1, :] = 0.0
            return hs

        handle = layer_mod.register_forward_hook(hook_fn)

    with torch.no_grad():
        logits = model(**inputs).logits[0, -1]

    if handle is not None:
        handle.remove()

    scores = {}
    for letter in ["A", "B", "C", "D", "E"]:
        t = tok.encode(" " + letter, add_special_tokens=False)
        if len(t) == 0:
            scores[letter] = -1e9
        else:
            scores[letter] = float(logits[t[0]].item())
    return scores


def margin(scores: Dict[str, float], gold: str) -> float:
    others = [v for k, v in scores.items() if k != gold]
    return float(scores.get(gold, -1e9) - max(others))


def run_mechanistic_analysis(config: Config, data: List[dict], behavior_df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    ex_map = {ex["id"]: ex for ex in data}
    direct_df = behavior_df[behavior_df["condition"] == "direct"].copy()

    success_ids = direct_df[direct_df["correct"] == 1]["id"].tolist()
    failure_ids = direct_df[direct_df["correct"] == 0]["id"].tolist()
    random.Random(config.seed).shuffle(success_ids)
    random.Random(config.seed + 1).shuffle(failure_ids)

    k = min(30, len(success_ids), len(failure_ids))
    target_ids = success_ids[:k] + failure_ids[:k]

    tok, model, device = prepare_local_model(config.local_model)
    n_layers = len(model.transformer.h)

    rows = []
    for ex_id in tqdm(target_ids, desc="Mechanistic layer scan"):
        ex = ex_map[ex_id]
        prompt = build_local_prompt(ex)
        gold = ex["answerKey"]

        base_scores = option_logits(tok, model, device, prompt, layer_ablate=-1)
        base_margin = margin(base_scores, gold)
        group = "success" if ex_id in success_ids[:k] else "failure"

        for layer in range(n_layers):
            ab_scores = option_logits(tok, model, device, prompt, layer_ablate=layer)
            ab_margin = margin(ab_scores, gold)
            rows.append(
                {
                    "id": ex_id,
                    "group": group,
                    "layer": layer,
                    "base_margin": base_margin,
                    "ablated_margin": ab_margin,
                    "delta_margin": ab_margin - base_margin,
                }
            )

    mech_df = pd.DataFrame(rows)

    pivot = mech_df.groupby(["layer", "group"])["delta_margin"].mean().reset_index()
    succ = pivot[pivot["group"] == "success"].set_index("layer")["delta_margin"]
    fail = pivot[pivot["group"] == "failure"].set_index("layer")["delta_margin"]
    sep = (succ - fail).abs().fillna(0.0)
    target_layer = int(sep.idxmax())

    # Paired causal test: target layer vs random control layer deltas per example
    paired_rows = []
    control_layer = 0 if target_layer != 0 else 1
    for ex_id in target_ids:
        sub = mech_df[mech_df["id"] == ex_id]
        t_delta = float(sub[sub["layer"] == target_layer]["delta_margin"].iloc[0])
        c_delta = float(sub[sub["layer"] == control_layer]["delta_margin"].iloc[0])
        paired_rows.append({"id": ex_id, "target_delta": t_delta, "control_delta": c_delta})
    paired_df = pd.DataFrame(paired_rows)

    t_stat, p_t = stats.ttest_rel(paired_df["target_delta"], paired_df["control_delta"])
    try:
        w_stat, p_w = stats.wilcoxon(paired_df["target_delta"], paired_df["control_delta"])
    except Exception:
        w_stat, p_w = np.nan, np.nan

    # Cohen's d for paired differences
    diff = paired_df["target_delta"] - paired_df["control_delta"]
    d = float(diff.mean() / (diff.std(ddof=1) + 1e-8))

    stats_out = {
        "n_examples": int(len(paired_df)),
        "n_layers": int(n_layers),
        "target_layer": int(target_layer),
        "control_layer": int(control_layer),
        "paired_t_stat": float(t_stat),
        "paired_t_p": float(p_t),
        "wilcoxon_stat": float(w_stat) if not pd.isna(w_stat) else None,
        "wilcoxon_p": float(p_w) if not pd.isna(p_w) else None,
        "cohens_d_paired": d,
    }

    return mech_df, stats_out


def summarize_and_plot(config: Config, behavior_df: pd.DataFrame, judge_df: pd.DataFrame, mech_df: pd.DataFrame, mech_stats: dict) -> dict:
    out = {}

    # Behavior summary
    by_cond = behavior_df.groupby("condition")["correct"].agg(["mean", "std", "count"]).reset_index()
    out["accuracy_by_condition"] = by_cond.to_dict(orient="records")

    paired = behavior_df.pivot(index="id", columns="condition", values="correct").dropna()
    mc = mcnemar_exact(paired["direct"].values.astype(int), paired["cot"].values.astype(int))
    out["mcnemar"] = mc
    out["failure_flip_rate_direct_to_cot"] = float(mc["b"] / max(len(paired), 1))
    out["failure_flip_rate_cot_to_direct"] = float(mc["c"] / max(len(paired), 1))

    # Coherence analysis
    coh_summary = judge_df.groupby(["condition", "correct"])["coherent"].agg(["mean", "count"]).reset_index()
    out["coherence_summary"] = coh_summary.to_dict(orient="records")

    direct_j = judge_df[judge_df["condition"] == "direct"]
    coh_success = direct_j[direct_j["correct"] == 1]["coherent"].values
    coh_failure = direct_j[direct_j["correct"] == 0]["coherent"].values
    if len(coh_success) > 0 and len(coh_failure) > 0:
        u_stat, p_u = stats.mannwhitneyu(coh_success, coh_failure, alternative="two-sided")
    else:
        u_stat, p_u = np.nan, np.nan
    out["coherence_mannwhitney"] = {
        "u_stat": float(u_stat) if not pd.isna(u_stat) else None,
        "p_value": float(p_u) if not pd.isna(p_u) else None,
        "n_success": int(len(coh_success)),
        "n_failure": int(len(coh_failure)),
    }

    out["mechanistic_stats"] = mech_stats

    # Plots
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(6, 4))
    sns.barplot(data=by_cond, x="condition", y="mean", palette=["#4c78a8", "#f58518"])
    plt.ylim(0, 1)
    plt.ylabel("Accuracy")
    plt.title("Accuracy: Direct vs CoT")
    plt.tight_layout()
    plt.savefig("results/plots/accuracy_direct_vs_cot.png", dpi=200)
    plt.close()

    if len(judge_df) > 0:
        plt.figure(figsize=(7, 4))
        sns.barplot(data=judge_df, x="condition", y="coherent", hue="correct", palette="Set2")
        plt.ylim(0, 1)
        plt.ylabel("Coherence Rate")
        plt.title("Goal-Action Coherence by Condition and Correctness")
        plt.tight_layout()
        plt.savefig("results/plots/coherence_rates.png", dpi=200)
        plt.close()

    layer_plot = mech_df.groupby(["layer", "group"])['delta_margin'].mean().reset_index()
    plt.figure(figsize=(8, 4))
    sns.lineplot(data=layer_plot, x="layer", y="delta_margin", hue="group", marker="o")
    plt.axhline(0.0, color="black", linewidth=1)
    plt.title("Ablation Delta Margin by Layer")
    plt.ylabel("Delta Margin (ablated - base)")
    plt.tight_layout()
    plt.savefig("results/plots/layer_ablation_deltas.png", dpi=200)
    plt.close()

    with open("results/metrics.json", "w") as f:
        json.dump(out, f, indent=2)

    return out


def save_environment(config: Config) -> dict:
    env = {
        "timestamp": datetime.now().isoformat(),
        "python": os.popen("python --version").read().strip(),
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "gpu_names": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else [],
        "config": config.__dict__,
    }
    with open("results/config.json", "w") as f:
        json.dump(env, f, indent=2)
    return env


def main() -> None:
    set_seed(42)
    ensure_dirs()
    config = Config()

    env = save_environment(config)
    print("Environment:", json.dumps(env, indent=2))

    data = load_csqa_subset(config.sample_size, config.seed)
    behavior_df = run_behavioral_eval(config, data, Path("results/model_outputs/api_outputs_v2.jsonl"))
    behavior_df.to_csv("results/behavioral_results.csv", index=False)

    judge_df = run_coherence_judging(config, behavior_df, Path("results/model_outputs/coherence_judgments_v2.jsonl"))
    judge_df.to_csv("results/coherence_results.csv", index=False)

    mech_df, mech_stats = run_mechanistic_analysis(config, data, behavior_df)
    mech_df.to_csv("results/mechanistic_layer_scan.csv", index=False)

    summary = summarize_and_plot(config, behavior_df, judge_df, mech_df, mech_stats)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Done. Key summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
