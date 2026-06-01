"""Tiered cost optimization: a high-precision regex fast-path in front of the LLM.

Goal: skip the LLM on the easy, overwhelmingly-safe cases (a clean single
"detail amount", and obvious non-transactions) while routing EVERYTHING uncertain to
`extract()`. The router optimizes for *precision*: its only job is to be safe enough to
avoid the LLM. When in doubt → LLM. It must never emit a transaction the LLM wouldn't.

extract_tiered() has the same signature/contract as extract(); meta.path tells you
whether a row was 'fast_path' (free) or 'llm' (paid).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ner import extract, enforce_contract, MAX_INPUT_CHARS  # noqa: E402

# Cues that a nearby number is NOT money (age, time, phone, quantity, units, percent,
# temperature, lottery number, budget, address, installment count). Presence of any of
# these → don't trust the regex, route to LLM. This deny-list is the router's safety
# margin: when in doubt, the LLM (which is injection-hardened and reads context) decides.
NOT_MONEY = re.compile(
    r"(ปี|อายุ|โมง|นาฬิกา|เบอร์|โทร|ฟอง|ชิ้น|อัน|คน|ตัว|ครั้ง|ซม|กม|กิโล|%|เปอร์เซ็นต์|ขวบ"
    r"|องศา|อุณหภูมิ|หวย|ล็อตเตอรี่|เลขเด็ด|เลขที่|งบ|งวด|องค์)"
)
# Injection / structured-text / spoof markers → route to LLM (it's hardened; regex isn't).
RISK = re.compile(r"(ignore|instruction|system|prompt|forget|ลืม|คำสั่ง|[{}\[\]<>])", re.I)
# Thai number-words the regex can't read → route to LLM.
THAI_NUM_WORD = re.compile(
    r"(ศูนย์|หนึ่ง|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า|สิบ|ร้อย|พัน|หมื่น|แสน|ล้าน)"
)
# A money amount: either thousands-grouped (1,250 / 2,500) or a plain digit run (199 /
# 55555), with optional decimals. Not preceded by a digit/comma/minus so we don't split a
# number mid-way; negatives/refunds are handled by NEG_AMOUNT and routed to the LLM.
AMOUNT = re.compile(r"(?<![\d.,\-])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?!\d)")
NEG_AMOUNT = re.compile(r"-\s*\d")

# Strip trailing currency words so "<detail> <amount> บาท" fast-paths cleanly.
CURRENCY_TAIL = re.compile(r"(บาท|฿|thb|บ\.?)\s*$", re.I)


def _has_thai_or_alpha(s: str) -> bool:
    return bool(re.search(r"[A-Za-z฀-๿]", s))


def fast_path(text: str) -> tuple[dict | None, str]:
    """Try to answer without the LLM. Returns (result|None, reason).

    result is None  → "route to LLM" (the safe default).
    result is a dict → confident enough to emit it directly.
    """
    if not isinstance(text, str):
        return None, "non_string"
    t = text.strip()
    if not t:
        return {"transactions": []}, "empty"

    # Any risk marker, non-money cue, negative amount, or Thai number-word → LLM.
    if RISK.search(t):
        return None, "risk_marker"
    if NEG_AMOUNT.search(t):
        return None, "negative_amount"
    if NOT_MONEY.search(t):
        return None, "not_money_cue"
    if THAI_NUM_WORD.search(t) and not AMOUNT.search(t):
        return None, "thai_number_word"

    amounts = AMOUNT.findall(t)

    # Zero amounts + no number-words + no risk: a greeting/question/only-detail.
    # Safe to emit empty for free.
    if not amounts:
        if THAI_NUM_WORD.search(t):
            return None, "thai_number_word"  # might be a real amount in words
        return {"transactions": []}, "no_amount_empty"

    # More than one amount → segmentation territory, where errors live. Route to LLM.
    if len(amounts) > 1:
        return None, "multi_amount"

    # Exactly one amount. Pull the detail = everything around it, minus the number and a
    # trailing currency word. Require a non-trivial detail.
    amt = amounts[0]
    detail = t.replace(amt, " ", 1)
    detail = re.sub(r"[.\-]+", " ", detail)  # strip leftover ".-" baht shorthand
    detail = CURRENCY_TAIL.sub("", detail.strip()).strip()
    detail = re.sub(r"\s+", " ", detail)
    if not detail or not _has_thai_or_alpha(detail) or len(detail) > 80:
        return None, "weak_detail"

    # enforce_contract handles amount coercion (comma/decimal) + final shape.
    result = enforce_contract({"transactions": [{"amount": amt, "detail": detail}]})
    if not result["transactions"]:
        return None, "contract_rejected"
    return result, "single_clean"


def extract_tiered(
    text: Any, model: str = "openai/gpt-4o-mini", **kw
) -> tuple[dict, dict]:
    """Drop-in tiered version of extract(). meta.path in {'fast_path','llm'}."""
    if isinstance(text, str) and len(text) <= MAX_INPUT_CHARS:
        fp, reason = fast_path(text)
        if fp is not None:
            return fp, {"path": "fast_path", "reason": reason, "model": "regex",
                        "latency_ms": 0.0, "cost_usd": 0.0, "error": None}
    result, meta = extract(text, model=model, **kw)
    meta["path"] = "llm"
    return result, meta


if __name__ == "__main__":
    import json
    import sys

    text = " ".join(sys.argv[1:]) or "ข้าวมันไก่ 50"
    fp, reason = fast_path(text)
    print(json.dumps({"text": text, "fast_path": fp, "reason": reason},
                     ensure_ascii=False, indent=2))
