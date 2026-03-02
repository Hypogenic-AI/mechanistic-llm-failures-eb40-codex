# Mechanistic Interpretability of Commonsense Reasoning Failures in LLMs

## 1. Executive Summary
This study tested whether commonsense failures come from missing knowledge or from breakdowns in goal-action coherence integration.

Using 120 CommonsenseQA validation items, GPT-4.1 achieved similar accuracy with direct prompting (90.0%) and CoT prompting (89.2%), with low bidirectional failure flips (direct→CoT 2.5%, CoT→direct 1.7%; McNemar p=1.0). In a local mechanistic proxy (`distilgpt2`, layer ablation on matched success/failure subsets), we found no statistically significant targeted-layer causal effect (paired t-test p=0.853, Wilcoxon p=0.546).

Practical implication: on this sampled setting, we do not find strong evidence that CoT triggers broad commonsense degradation; mechanistic signal localization remains weak with this small open-model proxy and requires stronger models/tasks.

## 2. Goal
### Hypothesis
Commonsense failures are not only missing-knowledge failures; they arise from internal breakdowns in goal-action coherence integration.

### Why Important
If true, debugging should target internal circuits/representations instead of only adding more data.

### Problem Solved
Provides an end-to-end paired protocol linking behavioral outcomes (real API model) and internal intervention outcomes (open model).

### Expected Impact
Helps separate behavioral failure claims from mechanism-level evidence and identifies where current methods are insufficient.

## 3. Data Construction
### Dataset Description
- Source: HuggingFace `commonsense_qa` (local disk snapshot in `datasets/commonsense_qa`)
- Split used: validation
- Full split size: 1,221
- Experiment sample: 120 items (seed=42)
- Task: 5-way multiple-choice commonsense QA

### Example Samples
| ID | Question (truncated) | Choices | Gold |
|---|---|---|---|
| `1afa02df...` | A revolving door is convenient... security measure at a what? | A bank / B library / C department store / D mall / E new york | A |
| `a7ab0860...` | What do people aim to do at work? | A complete job / B learn from each other / C kill animals / D wear hats / E talk to each other | A |

### Data Quality
- Missing values: 0% on used fields (`question`, `choices`, `answerKey`)
- Invalid model predictions (non A-E): 0
- Outliers: N/A for categorical QA
- Validation checks: option labels present, exactly 5 options per sample, answer key in A-E

### Preprocessing Steps
1. Loaded validation split from local arrow format via `datasets.load_from_disk`.
2. Deterministically shuffled indices with seed=42.
3. Selected first 120 examples for API evaluation.
4. Formatted each as fixed multiple-choice prompt with labeled options A-E.

### Train/Val/Test Splits
No training. Evaluation-only study on validation subset.

## 4. Experiment Description
### Methodology
#### High-Level Approach
1. Evaluate real LLM behavior on identical items under two prompt conditions (direct vs CoT).
2. Quantify flips and significance with paired tests.
3. Judge goal-action coherence for sampled predictions.
4. Run local causal proxy via layer ablations in a small open model on matched success/failure items.

#### Why This Method
- Real API model avoids simulated-agent artifacts.
- Paired per-item comparison controls content variance.
- Causal ablation provides intervention evidence (not only correlation).

Alternatives considered but not used now:
- Head-level activation patching in larger models (higher complexity/time).
- Multi-dataset expansion (deferred to follow-up).

### Implementation Details
#### Tools and Libraries
- Python: 3.12.8
- openai: 2.24.0
- torch: 2.7.1+cu126
- transformers: 4.51.3
- datasets: 4.6.1
- scipy: 1.17.1
- statsmodels: 0.14.6
- pandas: 3.0.1
- matplotlib/seaborn for plots

#### Algorithms/Models
- Behavioral model: `gpt-4.1` (API)
- Judge model: `gpt-4.1`
- Mechanistic proxy model: `distilgpt2` (6 transformer layers)

#### Hyperparameters
| Parameter | Value | Selection Method |
|---|---:|---|
| seed | 42 | fixed default |
| sample_size | 120 | runtime-quality tradeoff |
| judge_subset | 80 items (160 condition-rows) | cost/runtime tradeoff |
| temperature | 0.0 | deterministic evaluation |
| direct max_tokens | 16 | minimal output length |
| CoT max_tokens | 200 | allow short rationale |
| judge max_tokens | 120 | JSON judgment + brief reason |

#### Training / Analysis Pipeline
1. Build prompt for each item.
2. Query `gpt-4.1` under direct and CoT conditions.
3. Parse final answer robustly (CoT requires `FINAL_ANSWER: <A-E>`).
4. Compute paired correctness and McNemar exact test.
5. Judge coherence on subset.
6. Select matched success/failure items from direct condition.
7. Run per-layer residual ablation at final token in `distilgpt2`.
8. Compare targeted-layer effect vs control layer.

### Experimental Protocol
#### Reproducibility Information
- Runs for averaging: 1 primary + 1 cached validation rerun
- Seeds: [42]
- Hardware: 2x NVIDIA RTX 3090 (24GB each)
- Batch strategy: API-only behavioral calls; local mechanistic pass on GPU
- Mixed precision: not required (inference-only)
- Runtime: ~5 min API eval + ~2 min judging + ~1 min mechanistic scan

#### Evaluation Metrics
- Accuracy: fraction correct by condition.
- Failure-flip rates: direct-correct/CoT-wrong and reverse.
- McNemar exact p-value: paired condition significance.
- Coherence rate: judged 0/1 consistency between likely question goal and chosen option.
- Delta margin: `(ablated margin - base margin)` where margin = logit(gold) - max(logit(other)).

### Raw Results
#### Tables
| Method | Accuracy | 95% CI (Wilson) | N |
|---|---:|---|---:|
| Direct | 0.900 | [0.833, 0.942] | 120 |
| CoT | 0.892 | [0.823, 0.936] | 120 |

| Flip Type | Rate | Count |
|---|---:|---:|
| Direct correct → CoT wrong | 0.025 | 3 |
| CoT correct → Direct wrong | 0.0167 | 2 |

McNemar exact: `b=3`, `c=2`, `n_discordant=5`, `p=1.0`.

| Mechanistic Test | Value |
|---|---:|
| n_examples (matched) | 24 |
| n_layers | 6 |
| target_layer | 3 |
| paired t-test p | 0.853 |
| Wilcoxon p | 0.546 |
| Cohen's d (paired) | 0.038 |

#### Visualizations
- `results/plots/accuracy_direct_vs_cot.png`
- `results/plots/coherence_rates.png`
- `results/plots/layer_ablation_deltas.png`

#### Output Locations
- Results JSON: `results/metrics.json`, `results/summary.json`
- CSVs: `results/behavioral_results.csv`, `results/coherence_results.csv`, `results/mechanistic_layer_scan.csv`
- Raw outputs: `results/model_outputs/api_outputs_v2.jsonl`, `results/model_outputs/coherence_judgments_v2.jsonl`
- Config/environment: `results/config.json`

## 5. Result Analysis
### Key Findings
1. Direct and CoT performance were very close (90.0% vs 89.2%); no significant paired difference.
2. Failure-flip rates were low in both directions (2.5% and 1.7%), contradicting a strong toxic-CoT effect in this sample.
3. Coherence judge scores saturated near 1.0 in most groups, offering little discriminative signal.
4. Layer-ablation causal proxy did not show a significant target-vs-control effect.

### Hypothesis Testing Results
- Behavioral degradation under CoT: **not supported** on this sample.
- Coherence breakdown signal: **inconclusive** due score saturation.
- Mechanistic causal localization: **not supported** (no significant effect).

### Comparison to Baselines
- Direct baseline slightly outperformed CoT by 0.83 points absolute (not significant).
- No practical advantage for CoT under the tested prompt template.

### Surprises and Insights
- Initial run showed extreme CoT failure due parsing bug; after parser fix, the effect disappeared.
- This reinforces that evaluation infrastructure quality (parsing/format constraints) can dominate apparent reasoning conclusions.

### Error Analysis
Representative direct failures:
- `22015315e7ff79386877828b4fa27799`: rug near front door, predicted E vs gold D.
- `896b25dc41f84357add1c798d4a96cd8`: seaweed location, predicted A vs gold C.

Representative direct→CoT flips:
- `047c2d8c65d297b39aa42821c1ca76a9`: direct B correct, CoT A wrong.
- `1b3d286458a7e7f069222de0376d06da`: direct C correct, CoT D wrong.

### Limitations
- Single benchmark subset (CommonsenseQA only in this run).
- Small mechanistic proxy model (`distilgpt2`) may not reflect GPT-4.1 internals.
- Layer-level ablation, not head-level/path-level patching.
- Coherence judge was weakly discriminative (ceiling effect).
- One seed and one primary API model.

### Threats to Validity
- Construct validity: judged coherence may not perfectly represent goal-action coherence.
- External validity: findings may not transfer to other datasets/tasks.
- Internal validity: model mismatch between API behavior and open-model mechanism limits causal inference strength.

## 6. Conclusions
On this experiment, commonsense failures did not show strong CoT-specific degradation, and we found no significant mechanistic causal effect in the chosen open-model proxy. The current evidence does not support a strong claim that goal-action coherence breakdown is the dominant failure mode under these settings.

Confidence is moderate for behavioral results (stable paired design, reproducible rerun) and low-to-moderate for mechanism claims (small proxy/model mismatch). Stronger evidence would require larger mechanistic-capable models, head/path interventions, and richer coherence annotations.

## 7. Next Steps
### Immediate Follow-ups
1. Expand to `winogrande` and `ARC-Challenge` with the same paired API protocol.
2. Replace coherence judge with human or rubric-validated annotations on a stratified subset.
3. Run head-level activation patching (TransformerLens) on a larger open model.

### Alternative Approaches
- Mediation analysis on internal representations across prompt conditions.
- Sparse autoencoder feature steering for coherence-related features.

### Broader Extensions
- Compare architecture families and instruction-tuning variants.
- Test whether training objectives can reduce flip rates without harming baseline accuracy.

### Open Questions
- Which intervention granularity (layer/head/feature) is most diagnostic for commonsense integration?
- Are coherence failures concentrated in specific question archetypes?

## References
- `literature_review.md`
- Li et al. (2024), *Focus on Your Question! Interpreting and Mitigating Toxic CoT Problems in Commonsense Reasoning*.
- Cabannes et al. (2024), *Iteration Head: A Mechanistic Study of Chain-of-Thought*.
- Hou et al. (2023), *Towards a Mechanistic Interpretation of Multi-Step Reasoning Capabilities of Language Models*.
