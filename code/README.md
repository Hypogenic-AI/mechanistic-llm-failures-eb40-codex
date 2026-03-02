# Cloned Repositories

## Repo 1: TransformerLens
- URL: https://github.com/TransformerLensOrg/TransformerLens
- Purpose: Core library for mechanistic interpretability (activation caching, patching, attention/head analysis).
- Location: `code/TransformerLens/`
- Key files:
  - `code/TransformerLens/README.md`
  - `code/TransformerLens/transformer_lens/`
  - `code/TransformerLens/demos/`
- Installation requirements:
  - `pip install transformer_lens`
- Notes:
  - Useful for probing head-level circuits behind commonsense failure cases.
  - Includes IOI and induction-head style analyses transferable to goal-action coherence studies.

## Repo 2: lm-evaluation-harness
- URL: https://github.com/EleutherAI/lm-evaluation-harness
- Purpose: Standardized evaluation framework for LLM benchmarks.
- Location: `code/lm-evaluation-harness/`
- Key files:
  - `code/lm-evaluation-harness/README.md`
  - `code/lm-evaluation-harness/lm_eval/tasks/`
  - `code/lm-evaluation-harness/docs/interface.md`
- Installation requirements:
  - Base: `pip install -e .`
  - HF backend: `pip install "lm_eval[hf]"`
- Notes:
  - Contains commonsense tasks like `hellaswag` and `arc_easy/arc_challenge`.
  - Recommended for baseline accuracy and CoT/non-CoT comparisons.

## Repo 3: baukit
- URL: https://github.com/davidbau/baukit
- Purpose: Lightweight tracing/editing tools for PyTorch model internals.
- Location: `code/baukit/`
- Key files:
  - `code/baukit/README.md`
  - `code/baukit/baukit/nethook.py`
  - `code/baukit/notebooks/`
- Installation requirements:
  - `pip install git+https://github.com/davidbau/baukit`
- Notes:
  - Fast path for activation tracing/interventions without adopting a larger framework.
  - Useful for causal mediation and token-position ablations.

## Validation Notes
- Repositories cloned successfully and README files inspected.
- Deep runtime validation was not executed for these repos in this phase to avoid heavy dependency/GPU setup.
