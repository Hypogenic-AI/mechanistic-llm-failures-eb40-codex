# Validation Checklist

## Code Validation
- [x] Full pipeline runs without errors (`python src/run_research.py`).
- [x] Cached rerun executed and reproduced identical summary metrics/hash.
- [x] Random seed set (`42`) and stored in `results/config.json`.
- [x] No hardcoded absolute paths in experiment code.
- [x] Evaluation-only workflow (no train/test leakage).

## Scientific Validation
- [x] Paired statistical test used for direct vs CoT (McNemar exact).
- [x] Nonparametric test used for coherence score comparison (Mann-Whitney U).
- [x] Paired causal effect tests reported (paired t-test + Wilcoxon).
- [x] Effect size reported (Cohen's d).
- [x] Limitations and alternative explanations documented in `REPORT.md`.

## Documentation Validation
- [x] `planning.md` includes Motivation & Novelty and full plan.
- [x] `REPORT.md` includes methods, metrics, results, limitations, next steps.
- [x] `README.md` includes quick reproduction instructions and key findings.
- [x] Plot/metric output paths documented.

## Output Validation
- [x] Core outputs generated in `results/`.
- [x] Raw API/judge outputs cached in `results/model_outputs/`.
- [x] Figures generated in `results/plots/`.
