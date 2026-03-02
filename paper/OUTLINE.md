# Outline: Mechanistic Interpretability of Commonsense Reasoning Failures in LLMs

## Title
- Mechanistic Interpretability of Commonsense Reasoning Failures in LLMs: A Paired Behavioral-Intervention Study

## Abstract
- Problem: whether commonsense failures are missing knowledge or coherence-integration failures.
- Approach: paired direct-vs-CoT API evaluation + coherence judgments + open-model layer ablation proxy.
- Results: no significant direct-vs-CoT gap; low flip rates; no significant targeted-layer effect.
- Significance: cautions against strong toxic-CoT claims in this setting and motivates stronger mechanistic probes.

## Introduction
- Hook: commonsense failures matter for real deployments.
- Gap: prior studies rarely pair behavior and interventions on matched examples.
- Approach overview and quantitative preview.
- Contributions (3-4 bullets).
- Organization sentence.

## Related Work
- Toxic CoT and question-signal loss.
- Mechanistic studies of reasoning circuits and iteration heads.
- Causal mediation and steering approaches.
- Positioning of this work.

## Methodology
- Hypothesis and problem setup.
- Dataset and sampling details.
- Prompt conditions and parsing.
- Coherence judging protocol.
- Mechanistic proxy ablation and statistics.

## Results
- Accuracy/CI and McNemar table.
- Flip rates table.
- Mechanistic test table.
- Three figures with interpretation.

## Discussion
- Interpretation of null findings.
- Infrastructure lesson (parser bug).
- Limitations and threats to validity.
- Broader implications.

## Conclusion
- Summary, key takeaway, and concrete future directions.
