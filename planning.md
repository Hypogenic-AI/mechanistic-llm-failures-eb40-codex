# Research Plan: Mechanistic Interpretability of Commonsense Reasoning Failures in LLMs

## Motivation & Novelty Assessment

### Why This Research Matters
Commonsense failures in LLMs can cause incorrect real-world recommendations even when relevant facts are present, which limits reliability in assistant and agent settings. If failures are caused by internal integration breakdowns rather than missing facts, interventions should target mechanisms (attention pathways, representations, or training objectives) instead of only scaling data. This work helps model developers prioritize debugging and alignment strategies with mechanistic evidence.

### Gap in Existing Work
Prior work and the provided literature review show strong behavioral evidence (e.g., toxic CoT/failure flips) and isolated mechanism studies (iteration heads, reasoning probes), but there is limited unified evaluation connecting behavior-level commonsense failures to internal goal-action coherence signals on the same examples. Most studies do not jointly test: (1) direct vs CoT failure behavior, (2) causal intervention effects, and (3) whether API model failures can be mapped to open-model mechanistic signatures under matched prompts.

### Our Novel Contribution
We introduce a paired behavioral-mechanistic protocol for commonsense QA: identify failure/success pairs on real API models, score goal-action coherence in outputs, and then run activation-level causal analyses in a local transformer on matched prompts to localize layers/heads associated with coherent action selection. This directly tests whether failures align with reduced coherence-sensitive activation pathways, not only missing factual knowledge.

### Experiment Justification
- Experiment 1: Behavioral failure mapping on real APIs (Direct vs CoT)
  - Why needed: establishes whether failures persist despite factual availability and whether CoT helps or harms.
- Experiment 2: Goal-action coherence scoring and failure taxonomy
  - Why needed: operationalizes the central construct of the hypothesis and distinguishes knowledge errors from coherence integration errors.
- Experiment 3: Mechanistic contrastive analysis (success vs failure) on open model internals
  - Why needed: localizes where coherence-related separation emerges or collapses across layers/heads.
- Experiment 4: Causal intervention (targeted head ablation/patching)
  - Why needed: tests whether identified components are causally relevant, not just correlational.
- Experiment 5: Robustness and alternative explanations
  - Why needed: checks if effects are stable across prompt format, seed, and subset composition to separate architectural vs prompt-induced artifacts.

## Research Question
Do commonsense reasoning failures in LLMs primarily reflect missing knowledge, or do they stem from internal breakdowns in integrating goal-action coherence signals during inference?

## Background and Motivation
The project tests a mechanistic hypothesis motivated by the literature synthesis: commonsense failures often occur even when component facts are present, suggesting integration failure. We use pre-downloaded commonsense benchmarks and mechanistic tools in `code/TransformerLens` and `code/baukit` to connect observed errors to internals.

## Hypothesis Decomposition
- H1 (mechanistic): Failure examples show weaker internal separation between coherent and incoherent action options than success examples.
- H2 (causal): Intervening on identified coherence-related components significantly changes coherent-option probability.
- H3 (behavioral): CoT does not uniformly improve commonsense accuracy; in a nontrivial subset it degrades performance (failure flips).
- H0 (null): Observed failures are fully explained by missing knowledge/noise; no systematic mechanistic coherence signal differences.

Independent variables:
- Prompt condition: direct vs CoT.
- Example type: success vs failure pair.
- Intervention: none vs targeted ablation/patching.

Dependent variables:
- Accuracy.
- Failure-flip rate.
- Goal-action coherence score.
- Logit margin/probability for coherent option.
- Intervention delta.

Alternative explanations:
- Output-format sensitivity rather than reasoning quality.
- Dataset ambiguity or annotation noise.
- Open-model mismatch with API model behavior.

## Proposed Methodology

### Approach
A two-track design:
1. Real-model behavioral evaluation with API calls (required for LLM behavior validity).
2. Mechanistic tracing in an open transformer on matched prompts for causal localization.

This combines ecological validity (real API models) with internal access (open model).

### Experimental Steps
1. Environment verification and dependency setup with `uv` in local `.venv`.
2. Build a balanced evaluation subset from `commonsense_qa` and `winogrande` validation splits.
3. Query GPT-family API with direct and CoT prompts, fixed decoding params, and parse MC answers.
4. Compute accuracy, failure flips, and coherence score (rule-based rubric over action-goal consistency).
5. Run local mechanistic analysis on selected contrastive items with TransformerLens (per-layer residual/readout + head ablations).
6. Quantify causal effects: change in coherent-option logit/probability after targeted interventions.
7. Run robustness checks across 3 random seeds and prompt paraphrases.

### Baselines
- Direct-answer prompting baseline.
- CoT prompting baseline.
- Random-choice baseline (chance level).
- Untargeted/random head ablation control.

### Evaluation Metrics
- Accuracy (overall and by dataset).
- Failure-flip rate: `%` where direct correct but CoT wrong (and reverse).
- Goal-action coherence score (0/1 rubric per sample).
- Coherence logit margin: coherent option minus best incoherent option.
- Intervention effect size (Cohen's d, paired differences).

### Statistical Analysis Plan
- Paired comparison direct vs CoT accuracy: McNemar test.
- Coherence score success vs failure: Mann-Whitney U (nonparametric).
- Intervention effect on coherent margin: paired t-test or Wilcoxon depending on normality.
- Significance threshold: alpha = 0.05 with Benjamini-Hochberg correction for multiple component tests.
- Report 95% CI and effect size (Cohen's d or rank-biserial).

## Expected Outcomes
Support for hypothesis if:
- Nontrivial failure-flip rate appears despite factual clues.
- Failure examples show significantly lower coherence margins/signals.
- Targeted interventions produce significant directional changes in coherent-option probability.

Refutation if:
- Failures are random or fully explained by unknown facts.
- No consistent internal differences between success/failure.
- Interventions fail to affect outputs beyond noise.

## Timeline and Milestones
- Phase 1 (planning/documentation): 25 min.
- Phase 2 (setup + EDA): 20 min.
- Phase 3 (pipeline implementation): 70 min.
- Phase 4 (experiments): 70 min.
- Phase 5 (analysis/plots/stats): 40 min.
- Phase 6 (reporting/validation): 30 min.
- Buffer: ~30% distributed across phases for debugging/API retries.

## Potential Challenges
- API latency/rate limits: use retry/backoff and output caching.
- Answer parsing errors: strict format prompts + regex fallback.
- Mechanistic runtime costs: limit to high-value contrastive subset, use GPU and batched inference.
- Model mismatch (API vs open model): explicitly treat as construct-validity limitation and compare relative patterns.

## Success Criteria
- Reproducible pipeline runs end-to-end from local scripts.
- Statistical evidence for/against each sub-hypothesis with confidence intervals.
- At least one causal intervention result with significant directional effect or clear null.
- Complete `REPORT.md` and `README.md` with actual tables/figures and paths to artifacts.
