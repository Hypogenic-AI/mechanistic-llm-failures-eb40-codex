# Literature Review: Mechanistic Interpretability of Commonsense Reasoning Failures in LLMs

## Review Scope

### Research Question
Where do commonsense reasoning failures in LLMs originate mechanistically: missing knowledge, faulty integration of question-goal information, brittle iterative reasoning circuits, or training-induced shortcuts?

### Inclusion Criteria
- Mechanistic interpretability studies of transformer reasoning behavior.
- Papers analyzing CoT or multi-step reasoning internals.
- Papers with relevance to commonsense QA or reasoning benchmarks.
- 2023-2026 emphasis, with benchmark/foundational context where needed.

### Exclusion Criteria
- Pure prompting papers with no mechanistic analysis.
- Non-language-model interpretability work.
- Papers unavailable in full text and without sufficient abstract-level detail.

### Time Frame
- Primary: 2023-2026.

### Sources
- Paper-finder service (`.claude/skills/paper-finder/scripts/find_papers.py`)
- Semantic Scholar links returned by paper-finder
- arXiv fallback downloads

## Search Log

| Date | Query | Source | Results | Notes |
|------|-------|--------|---------|-------|
| 2026-03-02 | mechanistic interpretability language models reasoning | paper-finder (fast/json) | 75 ranked papers | Main usable ranked set |
| 2026-03-02 | commonsense reasoning failures large language models | paper-finder | timed out | Backend hang for this query |
| 2026-03-02 | goal action coherence planning language models | paper-finder | timed out | Backend hang for this query |

## Screening Results

- Total ranked papers (from successful query): 75
- Relevance >= 2 (target set): 57
- Successfully downloaded PDFs: 24
- Access/link failures: 33 (documented in `papers/download_log.json`)

## Key Papers

### Paper 1: Focus on Your Question! Interpreting and Mitigating Toxic CoT Problems in Commonsense Reasoning
- **Authors**: Jiachun Li et al.
- **Year**: 2024
- **Source**: arXiv/ACL-style publication track
- **Key Contribution**: Defines and quantifies Toxic CoT (cases where CoT flips correct direct answers to wrong answers) and proposes mitigation.
- **Methodology**: Attribution tracing + causal tracing over attention pathways; introduces RIDERS (Residual decoding + serial-position swap).
- **Datasets Used**: WinoGrande, CommonsenseQA, HellaSwag, SIQA, PIQA.
- **Results**: Reports toxic-rate reduction and overall accuracy gain (table indicates avg ACC gain and substantial toxic-rate drop).
- **Code Available**: Not clearly resolved from extracted text.
- **Relevance to Our Research**: Directly supports hypothesis that failures come from integration breakdowns (question signal loss) rather than only missing knowledge.

### Paper 2: Towards a Mechanistic Interpretation of Multi-Step Reasoning Capabilities of Language Models
- **Authors**: Yifan Hou et al.
- **Year**: 2023
- **Source**: EMNLP 2023
- **Key Contribution**: Proposes MechanisticProbe to recover implicit reasoning-tree structure from attention for procedural reasoning.
- **Methodology**: Attention-flow probing on GPT-2 (synthetic k-th smallest task) and LLaMA (ProofWriter, ARC).
- **Datasets Used**: Synthetic procedural data, ProofWriter, AI2 ARC.
- **Results**: Probe can recover reasoning-tree signals in many examples; indicates true multi-step computation in some cases.
- **Code Available**: Not confirmed from local extraction.
- **Relevance to Our Research**: Supports representational/circuit-level explanations over pure knowledge-deficit explanations.

### Paper 3: Iteration Head: A Mechanistic Study of Chain-of-Thought
- **Authors**: Vivien Cabannes et al.
- **Year**: 2024
- **Source**: NeurIPS
- **Key Contribution**: Identifies “iteration heads” as specialized attention mechanisms enabling iterative computation in CoT-like settings.
- **Methodology**: Controlled synthetic tasks (copying/parity/polynomial iteration), layer/head dissection, scaling studies.
- **Datasets Used**: Synthetic algorithmic tasks.
- **Results**: CoT and multi-layer setups enable longer iterative reasoning; interpretable circuit motif emerges.
- **Code Available**: Indicated in checklist text (codebase referenced).
- **Relevance to Our Research**: Strong architectural/circuit evidence for failure modes when iterative circuits are absent or unstable.

### Paper 4: How do Language Models Bind Entities in Context?
- **Authors**: (from paper-finder metadata)
- **Year**: 2023
- **Source**: Mechanistic interpretability literature
- **Key Contribution**: Entity-binding mechanism analysis.
- **Methodology**: Internal representation/head behavior analysis.
- **Datasets Used**: Contextual binding tasks.
- **Results**: Finds specific mechanisms for contextual entity tracking.
- **Code Available**: Unknown.
- **Relevance to Our Research**: Entity-goal binding quality can influence action coherence in commonsense tasks.

### Paper 5: A Mechanistic Analysis of a Transformer Trained on a Symbolic Multi-Step Reasoning Task
- **Authors**: (from paper-finder metadata)
- **Year**: 2024
- **Source**: arXiv
- **Key Contribution**: Circuit-level study of symbolic multi-step reasoning.
- **Methodology**: Synthetic symbolic tasks + mechanism tracing.
- **Datasets Used**: Symbolic synthetic tasks.
- **Results**: Shows decomposable reasoning subcircuits.
- **Code Available**: Unknown.
- **Relevance to Our Research**: Useful for architecture-vs-training disentanglement in controlled settings.

### Paper 6: A Mechanistic Interpretation of Arithmetic Reasoning in Language Models using Causal Mediation Analysis
- **Authors**: (from paper-finder metadata)
- **Year**: 2023
- **Source**: arXiv
- **Key Contribution**: Uses causal mediation analysis for arithmetic circuits.
- **Methodology**: Mediator interventions and pathway attribution.
- **Datasets Used**: Arithmetic tasks.
- **Results**: Isolates pathways that mediate reasoning outputs.
- **Code Available**: Unknown.
- **Relevance to Our Research**: Method transferable to commonsense goal-action mediation.

### Paper 7: Reasoning Circuits in Language Models: A Mechanistic Interpretation of Syllogistic Inference
- **Authors**: (from paper-finder metadata)
- **Year**: 2024
- **Source**: arXiv
- **Key Contribution**: Circuit analysis of deductive/syllogistic reasoning.
- **Methodology**: Circuit tracing and targeted interventions.
- **Datasets Used**: Syllogistic inference tasks.
- **Results**: Identifies reusable deductive sub-circuits.
- **Code Available**: Unknown.
- **Relevance to Our Research**: Bridges deductive mechanisms with commonsense inference failures.

### Paper 8: Understanding Reasoning in Thinking Language Models via Steering Vectors
- **Authors**: (from paper-finder metadata)
- **Year**: 2025
- **Source**: arXiv
- **Key Contribution**: Uses steering vectors to control/diagnose reasoning behavior.
- **Methodology**: Representation steering and behavior evaluation.
- **Datasets Used**: Reasoning benchmarks.
- **Results**: Demonstrates controllable shifts in reasoning outputs.
- **Code Available**: Unknown.
- **Relevance to Our Research**: Practical mechanism to test causal role of goal-action coherence features.

## Deep Reading Notes (Chunked Full-PDF Pass)

Full chunk-by-chunk passes were performed for:
- `2024_Focus_on_Your_Question_...` (9 chunks)
- `2023_Towards_a_Mechanistic_Interpretation_of_Multi-Step_...` (6 chunks)
- `2024_Iteration_Head_...` (8 chunks)

Raw extraction notes: `papers/deep_reading_raw_notes.md`.

Key extracted details:
- Toxic CoT work presents explicit evidence of early-layer question information loss during rationale generation; mitigation alters sequence positioning and decoding residuals.
- MechanisticProbe work argues that procedural reasoning signals can be recovered as tree-like structures from attention, suggesting internal algorithmic traces beyond memorization.
- Iteration Head work shows specific head-level iterative motifs emerging under CoT-compatible training setups and architecture depth.

## Common Methodologies

- **Attention/path tracing and causal interventions**: Used in Toxic CoT and causal-path papers.
- **Circuit-level head analysis**: Used in Iteration Head, syllogistic/deductive circuit papers.
- **Synthetic controllable tasks**: Used to separate architecture from data confounds.
- **Representation steering/mediation**: Emerging method for causal tests of internal features.

## Standard Baselines

- **Direct answer prompting (no CoT)**: Baseline to quantify CoT gains/failures.
- **CoT + self-consistency variants**: Strong prompting baseline.
- **Simple model scale baselines (small vs medium)**: To test capacity effects.
- **Task benchmark baselines**: Existing leaderboard metrics on CSQA/HellaSwag/WinoGrande/ARC.

## Evaluation Metrics

- **Accuracy (ACC)**: Primary outcome on commonsense QA.
- **Toxic Rate / failure-flip rate**: Fraction of cases where CoT hurts correctness.
- **Mechanistic probe score / pathway attribution strength**: Internal-mechanism metric.
- **Intervention delta**: Accuracy or logit shifts after ablation/patching/steering.

## Datasets in the Literature

- **CommonsenseQA, HellaSwag, WinoGrande, SIQA, PIQA**: Main commonsense benchmarks for CoT failure analysis.
- **AI2 ARC (Challenge/Easy)**: Often used for multi-step reasoning tests.
- **ProofWriter / synthetic procedural data**: Controlled mechanistic testing.

## Gaps and Opportunities

- Limited direct work on **goal-action coherence circuits** as a named construct.
- Many studies isolate arithmetic/symbolic reasoning; fewer connect to naturalistic commonsense failures.
- Training-data leakage vs mechanism still incompletely separated in open-domain settings.
- Need unified experiments combining: behavior metrics + mechanistic probes + causal interventions on the same examples.

## Recommendations for Our Experiment

- **Recommended datasets**:
  - Primary: CommonsenseQA, HellaSwag, WinoGrande, ARC-Challenge.
  - Diagnostic: TruthfulQA (multiple_choice) for confabulation pressure.
- **Recommended baselines**:
  - Direct answer, CoT, self-consistency.
  - Mechanistic intervention variants (head ablation, activation patching, steering vectors).
- **Recommended metrics**:
  - Accuracy, failure-flip/Toxic Rate, calibration, intervention delta.
- **Methodological considerations**:
  - Pair each failure case with matched success case.
  - Trace question-token information flow across layers and test causal impact.
  - Run architecture-controlled studies (small model + synthetic tasks) to separate training vs architecture effects.
