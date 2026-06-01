# NER Eval Report

_Placeholder. Generated for real by:_

```bash
export OPENROUTER_API_KEY=sk-or-...      # or put it in .env
uv run python src/eval.py
```

This overwrites the file with the live model-comparison table, per-bucket breakdown,
failure taxonomy, latency, and cost. Until then, run the offline checks:

```bash
uv run python src/eval.py --selftest     # 18/18 graceful-degradation checks, no key
```
