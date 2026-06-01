# Tiered Cost-Optimization Report

Regex fast-path → `openai/gpt-4o-mini` fallback, vs pure `openai/gpt-4o-mini`, on 62 messages.

| Metric | Pure LLM | Tiered | Δ |
|---|---|---|---|
| Txn F1 | 0.853 | 0.729 | -0.124 |
| Amount F1 | 0.930 | 0.930 | +0.000 |
| Detail F1 | 0.853 | 0.729 | -0.124 |
| Exact-match | 90.3% | 77.4% | -12.9 pts |
| LLM calls | 60 | 29 | -31 |
| $/1k msgs | $0.107 | $0.051 | -52% |

- **Fast-pathed (no LLM): 33/62 = 53%** — the cost win.
- **Fast-path-induced regressions (kill metric): NONE ✅**
- Pure injection leaks: 0 | Tiered injection leaks: 0