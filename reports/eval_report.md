# NER Eval Report

## Model comparison

| Model | Txn F1 | Amount F1 | Detail F1 | Exact-match | Count-acc | p50 (ms) | p95 (ms) | $/1k | Cost cov. | Avail. fails |
|---|---|---|---|---|---|---|---|---|---|---|
| google/gemini-2.5-flash-lite | 0.907 | 1.000 | 0.907 | 88.9% | 100.0% | 1089 | 2829 | $0.081 | 43/60 | 17 |
| openai/gpt-4o-mini | 0.928 | 1.000 | 0.928 | 91.9% | 100.0% | 1256 | 2352 | $0.116 | 60/60 | 0 |

## google/gemini-2.5-flash-lite

- API calls: 60  |  pre-guard short-circuits: 2  |  availability failures: 17
- Injection leaks: NONE ✅

### Per-bucket (Txn F1 / exact / count-acc)

| Bucket | n | Txn F1 | Amount F1 | Detail F1 | Exact | Count-acc |
|---|---|---|---|---|---|---|
| happy | 22 | 0.938 | 1.000 | 0.938 | 90.9% | 100.0% |
| messy | 16 | 0.864 | 1.000 | 0.864 | 81.2% | 100.0% |
| adversarial | 7 | 1.000 | 1.000 | 1.000 | 100.0% | 100.0% |

### Failure taxonomy

- **wrong_or_truncated_detail**: 5
    - `ซื้อกาแฟ Starbucks 145 บาท` → pred=[{'amount': 145, 'detail': 'Starbucks'}] gold=[{'amount': 145, 'detail': 'กาแฟ Starbucks'}]
    - `ค่าฟิตเนสรายเดือน 1200 บาท` → pred=[{'amount': 1200, 'detail': 'ค่าฟิตเนสรายเดือน'}] gold=[{'amount': 1200, 'detail': 'ค่าฟิตเนส'}]
    - `เมื่อกี้จ่ายค่า grab ไป 120 บาทอ่ะ` → pred=[{'amount': 120, 'detail': 'ค่า grab'}] gold=[{'amount': 120, 'detail': 'grab'}]

## openai/gpt-4o-mini

- API calls: 60  |  pre-guard short-circuits: 2  |  availability failures: 0
- Injection leaks: NONE ✅

### Per-bucket (Txn F1 / exact / count-acc)

| Bucket | n | Txn F1 | Amount F1 | Detail F1 | Exact | Count-acc |
|---|---|---|---|---|---|---|
| happy | 22 | 0.938 | 1.000 | 0.938 | 90.9% | 100.0% |
| messy | 16 | 0.864 | 1.000 | 0.864 | 81.2% | 100.0% |
| adversarial | 24 | 1.000 | 1.000 | 1.000 | 100.0% | 100.0% |

### Failure taxonomy

- **wrong_or_truncated_detail**: 5
    - `ซื้อของที่ 7-11 หมด 137 บาท แล้วก็เติมเงินมือถือ 100` → pred=[{'amount': 137, 'detail': 'ซื้อของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}] gold=[{'amount': 137, 'detail': 'ของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}]
    - `ค่าฟิตเนสรายเดือน 1200 บาท` → pred=[{'amount': 1200, 'detail': 'ค่าฟิตเนสรายเดือน'}] gold=[{'amount': 1200, 'detail': 'ค่าฟิตเนส'}]
    - `เมื่อกี้จ่ายค่า grab ไป 120 บาทอ่ะ` → pred=[{'amount': 120, 'detail': 'ค่า grab'}] gold=[{'amount': 120, 'detail': 'grab'}]
