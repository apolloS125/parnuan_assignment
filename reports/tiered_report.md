# Tiered Cost-Optimization Report

Regex fast-path → `openai/gpt-4o-mini` fallback, vs pure `openai/gpt-4o-mini`, on 100 messages.

| Metric | Pure LLM | Tiered | Δ |
|---|---|---|---|
| Txn F1 | 0.925 | 0.730 | -0.195 |
| Amount F1 | 1.000 | 1.000 | +0.000 |
| Detail F1 | 0.925 | 0.730 | -0.195 |
| Exact-match | 91.0% | 69.6% | -21.4 pts |
| LLM calls | 98 | 57 | -41 |
| $/1k msgs | $0.116 | $0.029 | -75% |

- **Fast-pathed (no LLM): 43/100 = 43%** — the cost win.
- **Fast-path-induced regressions (kill metric): NONE ✅**
- Pure injection leaks: 0 | Tiered injection leaks: 0