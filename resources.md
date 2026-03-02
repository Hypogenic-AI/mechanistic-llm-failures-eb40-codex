# Resources Catalog

## Summary
This document catalogs all resources gathered for the research project, including papers, datasets, and code repositories.

### Search Strategy
- Primary search used paper-finder with a mechanistic reasoning query and relevance ranking.
- Download strategy: Semantic Scholar open-access PDF first, arXiv title-match fallback.
- Dataset strategy: prioritize HuggingFace benchmark datasets with local `save_to_disk` snapshots.
- Code strategy: clone reusable mech-interp and evaluation toolchains.

### Selection Criteria
- Relevance score >= 2 from paper-finder.
- Direct relevance to reasoning circuits, CoT behavior, or commonsense benchmark analysis.
- Availability of executable code or benchmark compatibility.

### Challenges Encountered
- Two paper-finder queries timed out; one query completed successfully.
- 33 ranked relevant papers had no resolvable open PDF URL in automated retrieval.
- Some HF datasets (`piqa`, `social_i_qa`) require legacy dataset scripts and were skipped in favor of equivalent benchmark-ready alternatives.

## Papers
Total papers downloaded: 24

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Fluid Representations in Reasoning Models | Dmitrii Kharlapenko, Alessandro Stolfo, Arthur Conmy, Mrinma... | 2026 | `papers/2026_Fluid_Representations_in_Reasoning_Models.pdf` | Mechanistic reasoning / CoT / circuits |
| Interpreting and Controlling LLM Reasoning through Integrated Policy Gradient | Changming Li, Kaixin Zhang, Haoyun Xu, Yingdong Shi, Zheng Z... | 2026 | `papers/2026_Interpreting_and_Controlling_LLM_Reasoning_through_Integrated_Policy_Gradient.pdf` | Mechanistic reasoning / CoT / circuits |
| Towards a Mechanistic Understanding of Propositional Logical Reasoning in Large Language Models | Da Chen, Qiyao Yan, Liangming Pan | 2026 | `papers/2026_Towards_a_Mechanistic_Understanding_of_Propositional_Logical_Reasoning_in_Large_Language_Models.pdf` | Mechanistic reasoning / CoT / circuits |
| Detection and Mitigation of Hallucination in Large Reasoning Models: A Mechanistic Perspective | ZhongXiang Sun, Qipeng Wang, Haoyu Wang, Xiao Zhang, Jun Xu | 2025 | `papers/2025_Detection_and_Mitigation_of_Hallucination_in_Large_Reasoning_Models_A_Mechanistic_Perspective.pdf` | Mechanistic reasoning / CoT / circuits |
| From Indirect Object Identification to Syllogisms: Exploring Binary Mechanisms in Transformer Circuits | Karim Saraipour | 2025 | `papers/2025_From_Indirect_Object_Identification_to_Syllogisms_Exploring_Binary_Mechanisms_in_Transformer_Circuits.pdf` | Mechanistic reasoning / CoT / circuits |
| How Chain-of-Thought Works? Tracing Information Flow from Decoding, Projection, and Activation | Hao Yang, Qing Zhao, Lei Li | 2025 | `papers/2025_How_Chain-of-Thought_Works_Tracing_Information_Flow_from_Decoding_Projection_and_Activation.pdf` | Mechanistic reasoning / CoT / circuits |
| How does Chain of Thought Think? Mechanistic Interpretability of Chain-of-Thought Reasoning with Sparse Autoencoding | Xi Chen, A. Plaat, N. V. Stein | 2025 | `papers/2025_How_does_Chain_of_Thought_Think_Mechanistic_Interpretability_of_Chain-of-Thought_Reasoning_with_Sparse_Autoencoding.pdf` | Mechanistic reasoning / CoT / circuits |
| Implicit Reasoning in Transformers is Reasoning through Shortcuts | Tianhe Lin, Jian Xie, Siyu Yuan, Deqing Yang | 2025 | `papers/2025_Implicit_Reasoning_in_Transformers_is_Reasoning_through_Shortcuts.pdf` | Mechanistic reasoning / CoT / circuits |
| Mechanistic Interpretability of LoRA-Adapted Language Models for Nuclear Reactor Safety Applications | Yoonpyo Lee | 2025 | `papers/2025_Mechanistic_Interpretability_of_LoRA-Adapted_Language_Models_for_Nuclear_Reactor_Safety_Applications.pdf` | Mechanistic reasoning / CoT / circuits |
| Mechanistic Unveiling of Transformer Circuits: Self-Influence as a Key to Model Reasoning | Lin Zhang, Lijie Hu, Di Wang | 2025 | `papers/2025_Mechanistic_Unveiling_of_Transformer_Circuits_Self-Influence_as_a_Key_to_Model_Reasoning.pdf` | Mechanistic reasoning / CoT / circuits |
| Toward Mechanistic Explanation of Deductive Reasoning in Language Models | Davide Maltoni, Matteo Ferrara | 2025 | `papers/2025_Toward_Mechanistic_Explanation_of_Deductive_Reasoning_in_Language_Models.pdf` | Mechanistic reasoning / CoT / circuits |
| Understanding Reasoning in Thinking Language Models via Steering Vectors | Constantin Venhoff, Iv'an Arcuschin, Philip Torr, Arthur Con... | 2025 | `papers/2025_Understanding_Reasoning_in_Thinking_Language_Models_via_Steering_Vectors.pdf` | Mechanistic reasoning / CoT / circuits |
| A Implies B: Circuit Analysis in LLMs for Propositional Logical Reasoning | Guan Zhe Hong, Nishanth Dikkala, Enming Luo, Cyrus Rashtchia... | 2024 | `papers/2024_A_Implies_B_Circuit_Analysis_in_LLMs_for_Propositional_Logical_Reasoning.pdf` | Mechanistic reasoning / CoT / circuits |
| A Mechanistic Analysis of a Transformer Trained on a Symbolic Multi-Step Reasoning Task | Jannik Brinkmann, A. Sheshadri, Victor Levoso, Paul Swoboda,... | 2024 | `papers/2024_A_Mechanistic_Analysis_of_a_Transformer_Trained_on_a_Symbolic_Multi-Step_Reasoning_Task.pdf` | Mechanistic reasoning / CoT / circuits |
| Causal Interventions on Causal Paths: Mapping GPT-2's Reasoning From Syntax to Semantics | Isabelle Lee, Joshua Lum, Ziyi Liu, Dani Yogatama | 2024 | `papers/2024_Causal_Interventions_on_Causal_Paths_Mapping_GPT-2_s_Reasoning_From_Syntax_to_Semantics.pdf` | Mechanistic reasoning / CoT / circuits |
| Focus on Your Question! Interpreting and Mitigating Toxic CoT Problems in Commonsense Reasoning | Jiachun Li, Pengfei Cao, Chenhao Wang, Zhuoran Jin, Yubo Che... | 2024 | `papers/2024_Focus_on_Your_Question_Interpreting_and_Mitigating_Toxic_CoT_Problems_in_Commonsense_Reasoning.pdf` | Mechanistic reasoning / CoT / circuits |
| Iteration Head: A Mechanistic Study of Chain-of-Thought | Vivien Cabannes, Charles Arnal, Wassim Bouaziz, Alice Yang, ... | 2024 | `papers/2024_Iteration_Head_A_Mechanistic_Study_of_Chain-of-Thought.pdf` | Mechanistic reasoning / CoT / circuits |
| Locate-then-edit for Multi-hop Factual Recall under Knowledge Editing | Zhuoran Zhang, Yongxiang Li, Zijian Kan, Keyuan Cheng, Lijie... | 2024 | `papers/2024_Locate-then-edit_for_Multi-hop_Factual_Recall_under_Knowledge_Editing.pdf` | Mechanistic reasoning / CoT / circuits |
| Pre-trained Large Language Models Use Fourier Features to Compute Addition | Tianyi Zhou, Deqing Fu, Vatsal Sharan, Robin Jia | 2024 | `papers/2024_Pre-trained_Large_Language_Models_Use_Fourier_Features_to_Compute_Addition.pdf` | Mechanistic reasoning / CoT / circuits |
| Reasoning Circuits in Language Models: A Mechanistic Interpretation of Syllogistic Inference | Geonhee Kim, Marco Valentino, André Freitas | 2024 | `papers/2024_Reasoning_Circuits_in_Language_Models_A_Mechanistic_Interpretation_of_Syllogistic_Inference.pdf` | Mechanistic reasoning / CoT / circuits |
| A Mechanistic Interpretation of Arithmetic Reasoning in Language Models using Causal Mediation Analysis | Alessandro Stolfo, Yonatan Belinkov, Mrinmaya Sachan | 2023 | `papers/2023_A_Mechanistic_Interpretation_of_Arithmetic_Reasoning_in_Language_Models_using_Causal_Mediation_Analysis.pdf` | Mechanistic reasoning / CoT / circuits |
| How do Language Models Bind Entities in Context? | Jiahai Feng, Jacob Steinhardt | 2023 | `papers/2023_How_do_Language_Models_Bind_Entities_in_Context.pdf` | Mechanistic reasoning / CoT / circuits |
| How does GPT-2 compute greater-than?: Interpreting mathematical abilities in a pre-trained language model | Michael Hanna, Ollie Liu, Alexandre Variengien | 2023 | `papers/2023_How_does_GPT-2_compute_greater-than_Interpreting_mathematical_abilities_in_a_pre-trained_language_model.pdf` | Mechanistic reasoning / CoT / circuits |
| Towards a Mechanistic Interpretation of Multi-Step Reasoning Capabilities of Language Models | Yifan Hou, Jiaoda Li, Yu Fei, Alessandro Stolfo, Wangchunshu... | 2023 | `papers/2023_Towards_a_Mechanistic_Interpretation_of_Multi-Step_Reasoning_Capabilities_of_Language_Models.pdf` | Mechanistic reasoning / CoT / circuits |

See `papers/README.md` for detailed descriptions and unresolved downloads.

## Datasets
Total datasets downloaded: 5

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| commonsense_qa | huggingface:commonsense_qa | train:9741, validation:1221, test:1140 | commonsense_multiple_choice | `datasets/commonsense_qa` | samples in `samples/examples.json` |
| hellaswag | huggingface:hellaswag | train:39905, test:10003, validation:10042 | commonsense_narrative_completion | `datasets/hellaswag` | samples in `samples/examples.json` |
| winogrande_winogrande_debiased | huggingface:winogrande/winogrande_debiased | train:9248, test:1767, validation:1267 | pronoun_coreference_commonsense | `datasets/winogrande_winogrande_debiased` | samples in `samples/examples.json` |
| allenai_ai2_arc_ARC-Challenge | huggingface:allenai/ai2_arc/ARC-Challenge | train:1119, test:1172, validation:299 | science_commonsense_qa | `datasets/allenai_ai2_arc_ARC-Challenge` | samples in `samples/examples.json` |
| truthful_qa_multiple_choice | huggingface:truthful_qa/multiple_choice | validation:817 | truthfulness_and_reasoning | `datasets/truthful_qa_multiple_choice` | samples in `samples/examples.json` |

See `datasets/README.md` for download instructions and loading examples.

## Code Repositories
Total repositories cloned: 3

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| TransformerLens | https://github.com/TransformerLensOrg/TransformerLens | Mechanistic interpretability library | `code/TransformerLens/` | Activation cache/patching, head-level analysis |
| lm-evaluation-harness | https://github.com/EleutherAI/lm-evaluation-harness | Benchmark evaluation framework | `code/lm-evaluation-harness/` | Use for CSQA/HellaSwag/ARC-style evaluations |
| baukit | https://github.com/davidbau/baukit | Tracing/intervention toolkit for PyTorch | `code/baukit/` | Lightweight hooks for causal interventions |

See `code/README.md` for key files and setup notes.

## Gaps and Workarounds
- Missing open-access PDFs are logged in `papers/download_log.json` and listed in `papers/README.md`.
- For script-based HF datasets that no longer load under current `datasets` version, substituted with benchmark-equivalent datasets that load cleanly.

## Recommendations for Experiment Design

1. **Primary dataset(s)**: `commonsense_qa`, `hellaswag`, `winogrande_winogrande_debiased`, `allenai_ai2_arc_ARC-Challenge`.
2. **Baseline methods**: direct answer prompting, CoT, self-consistency, and intervention-based variants (head ablation / activation patching).
3. **Evaluation metrics**: Accuracy, Toxic/failure-flip rate, and intervention delta under targeted circuit edits.
4. **Code to adapt/reuse**: use `TransformerLens` for mechanistic tracing, `baukit` for quick interventions, and `lm-evaluation-harness` for standardized scoring.
## Research Execution Update (2026-03-02)
- Implemented end-to-end experiment script: `src/run_research.py`.
- Behavioral evaluation used real API model `gpt-4.1` on 120 CommonsenseQA validation items (direct vs CoT).
- Coherence judgments were collected with `gpt-4.1` on 80 sampled items x 2 conditions.
- Mechanistic proxy analysis used local `distilgpt2` with layer-level residual ablations on matched success/failure subsets.
- Outputs written to `results/` and detailed findings documented in `REPORT.md`.
