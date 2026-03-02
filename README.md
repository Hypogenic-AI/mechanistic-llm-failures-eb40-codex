# Mechanistic Commonsense Failure Study

This project runs a full behavioral + mechanistic pipeline to test whether commonsense failures are caused by missing knowledge or by breakdowns in goal-action coherence integration.

## Key Findings
- GPT-4.1 accuracy was similar for direct vs CoT prompting on 120 CommonsenseQA items (0.900 vs 0.892).
- Failure flips were low and not significant (McNemar exact p=1.0).
- Local mechanistic proxy (`distilgpt2` layer ablations) found no significant targeted causal effect.
- Main takeaway: strong coherence-breakdown claims are not supported in this run; stronger mechanistic setups are needed.

## Reproduce
1. Activate environment:
   - `source .venv/bin/activate`
2. Run experiment:
   - `python src/run_research.py`
3. Inspect outputs:
   - `results/summary.json`
   - `results/metrics.json`
   - `results/plots/`
   - `REPORT.md`

## File Structure
- `src/run_research.py`: end-to-end experiment pipeline
- `planning.md`: motivation, novelty, and design plan
- `REPORT.md`: full methods/results/analysis
- `results/`: CSV/JSON outputs and plots
- `results/model_outputs/`: cached API responses and coherence judgments
