# NER Eval Report

## Model comparison

| Model | Txn F1 | Amount F1 | Detail F1 | Exact-match | Count-acc | p50 (ms) | p95 (ms) | $/1k | Cost cov. | Avail. fails |
|---|---|---|---|---|---|---|---|---|---|---|
| google/gemini-2.5-flash-lite | 0.921 | 0.993 | 0.921 | 90.3% | 98.4% | 1711 | 6386 | $0.074 | 60/60 | 0 |
| openai/gpt-4o-mini | 0.928 | 1.000 | 0.928 | 91.9% | 100.0% | 1250 | 2414 | $0.108 | 60/60 | 0 |

## google/gemini-2.5-flash-lite

- API calls: 60  |  pre-guard short-circuits: 2  |  availability failures: 0
- Injection leaks: NONE ✅

### Per-bucket (Txn F1 / exact / count-acc)

| Bucket | n | Txn F1 | Amount F1 | Detail F1 | Exact | Count-acc |
|---|---|---|---|---|---|---|
| happy | 22 | 0.938 | 1.000 | 0.938 | 90.9% | 100.0% |
| messy | 16 | 0.864 | 1.000 | 0.864 | 81.2% | 100.0% |
| adversarial | 24 | 0.968 | 0.968 | 0.968 | 95.8% | 95.8% |

### Failure taxonomy

- **wrong_or_truncated_detail**: 5
    - `ซื้อของที่ 7-11 หมด 137 บาท แล้วก็เติมเงินมือถือ 100` → pred=[{'amount': 137, 'detail': '7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}] gold=[{'amount': 137, 'detail': 'ของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}]
    - `ค่าฟิตเนสรายเดือน 1200 บาท` → pred=[{'amount': 1200, 'detail': 'ค่าฟิตเนสรายเดือน'}] gold=[{'amount': 1200, 'detail': 'ค่าฟิตเนส'}]
    - `เมื่อกี้จ่ายค่า grab ไป 120 บาทอ่ะ` → pred=[{'amount': 120, 'detail': 'ค่า grab'}] gold=[{'amount': 120, 'detail': 'grab'}]
- **hallucinated_txn**: 1
    - `ค่ากาแฟ -50 บาท` → pred=[{'amount': 50, 'detail': 'ค่ากาแฟ'}] gold=[]

## openai/gpt-4o-mini

- API calls: 60  |  pre-guard short-circuits: 2  |  availability failures: 0
- Injection leaks: NONE ✅

### Per-bucket (Txn F1 / exact / count-acc)

| Bucket | n | Txn F1 | Amount F1 | Detail F1 | Exact | Count-acc |
|---|---|---|---|---|---|---|
| happy | 22 | 0.906 | 1.000 | 0.906 | 86.4% | 100.0% |
| messy | 16 | 0.909 | 1.000 | 0.909 | 87.5% | 100.0% |
| adversarial | 24 | 1.000 | 1.000 | 1.000 | 100.0% | 100.0% |

### Failure taxonomy

- **wrong_or_truncated_detail**: 5
    - `ค่าเช่าบ้านเดือนนี้ 8500` → pred=[{'amount': 8500, 'detail': 'ค่าเช่าบ้านเดือนนี้'}] gold=[{'amount': 8500, 'detail': 'ค่าเช่าบ้าน'}]
    - `ซื้อของที่ 7-11 หมด 137 บาท แล้วก็เติมเงินมือถือ 100` → pred=[{'amount': 137, 'detail': 'ซื้อของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}] gold=[{'amount': 137, 'detail': 'ของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}]
    - `ค่าฟิตเนสรายเดือน 1200 บาท` → pred=[{'amount': 1200, 'detail': 'ค่าฟิตเนสรายเดือน'}] gold=[{'amount': 1200, 'detail': 'ค่าฟิตเนส'}]
