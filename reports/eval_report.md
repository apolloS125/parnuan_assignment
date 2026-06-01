# NER Eval Report

## Model comparison

| Model | Txn F1 | Amount F1 | Detail F1 | Exact-match | Count-acc | p50 (ms) | p95 (ms) | $/1k | Cost cov. | Avail. fails |
|---|---|---|---|---|---|---|---|---|---|---|
| openai/gpt-4o-mini | 0.925 | 1.000 | 0.925 | 91.0% | 100.0% | 1367 | 2314 | $0.116 | 98/98 | 0 |
| meta-llama/llama-3.3-70b-instruct | 0.827 | 0.900 | 0.827 | 80.0% | 88.0% | 1614 | 4165 | $0.089 | 98/98 | 0 |

## openai/gpt-4o-mini

- API calls: 98  |  pre-guard short-circuits: 2  |  availability failures: 0
- Injection leaks: NONE ✅

### Per-bucket (Txn F1 / exact / count-acc)

| Bucket | n | Txn F1 | Amount F1 | Detail F1 | Exact | Count-acc |
|---|---|---|---|---|---|---|
| happy | 32 | 0.926 | 1.000 | 0.926 | 87.5% | 100.0% |
| messy | 28 | 0.878 | 1.000 | 0.878 | 82.1% | 100.0% |
| adversarial | 40 | 1.000 | 1.000 | 1.000 | 100.0% | 100.0% |

### Failure taxonomy

- **wrong_or_truncated_detail**: 9
    - `ซื้อของที่ 7-11 หมด 137 บาท แล้วก็เติมเงินมือถือ 100` → pred=[{'amount': 137, 'detail': 'ซื้อของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}] gold=[{'amount': 137, 'detail': 'ของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}]
    - `ค่าฟิตเนสรายเดือน 1200 บาท` → pred=[{'amount': 1200, 'detail': 'ค่าฟิตเนสรายเดือน'}] gold=[{'amount': 1200, 'detail': 'ค่าฟิตเนส'}]
    - `เมื่อกี้จ่ายค่า grab ไป 120 บาทอ่ะ` → pred=[{'amount': 120, 'detail': 'ค่า grab'}] gold=[{'amount': 120, 'detail': 'grab'}]

## meta-llama/llama-3.3-70b-instruct

- API calls: 98  |  pre-guard short-circuits: 2  |  availability failures: 0
- Injection leaks: NONE ✅

### Per-bucket (Txn F1 / exact / count-acc)

| Bucket | n | Txn F1 | Amount F1 | Detail F1 | Exact | Count-acc |
|---|---|---|---|---|---|---|
| happy | 32 | 0.739 | 0.826 | 0.739 | 62.5% | 75.0% |
| messy | 28 | 0.886 | 0.962 | 0.886 | 85.7% | 96.4% |
| adversarial | 40 | 0.898 | 0.939 | 0.898 | 90.0% | 92.5% |

### Failure taxonomy

- **missed_all**: 11
    - `ข้าวมันไก่ 50` → pred=[] gold=[{'amount': 50, 'detail': 'ข้าวมันไก่'}]
    - `ส้มตำ 40 บาท` → pred=[] gold=[{'amount': 40, 'detail': 'ส้มตำ'}]
    - `ตั๋วหนัง 220` → pred=[] gold=[{'amount': 220, 'detail': 'ตั๋วหนัง'}]
- **wrong_or_truncated_detail**: 8
    - `ซื้อของที่ 7-11 หมด 137 บาท แล้วก็เติมเงินมือถือ 100` → pred=[{'amount': 137, 'detail': 'ซื้อของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}] gold=[{'amount': 137, 'detail': 'ของที่ 7-11'}, {'amount': 100, 'detail': 'เติมเงินมือถือ'}]
    - `จ่ายค่า Netflix 419` → pred=[{'amount': 419, 'detail': 'Netflix'}] gold=[{'amount': 419, 'detail': 'ค่า Netflix'}]
    - `ค่าฟิตเนสรายเดือน 1200 บาท` → pred=[{'amount': 1200, 'detail': 'ค่าฟิตเนสรายเดือน'}] gold=[{'amount': 1200, 'detail': 'ค่าฟิตเนส'}]
- **hallucinated_txn**: 1
    - `ค่ากาแฟ -50 บาท` → pred=[{'amount': 50, 'detail': 'ค่ากาแฟ'}] gold=[]
