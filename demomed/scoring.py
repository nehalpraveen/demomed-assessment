import re
from typing import Tuple, Any

def _parse_bp(s: Any) -> Tuple[int|None, int|None]:
    if not isinstance(s, str): return None, None
    m = re.match(r"^\s*(\d+)\s*/\s*(\d+)\s*$", s)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)

def bp_score(bp: Any) -> int:
    sys, dia = _parse_bp(bp)
    if sys is None or dia is None: return 0
    if sys >= 140 or dia >= 90: return 3
    if sys >= 130 or dia >= 80: return 2
    if sys >= 120 and dia < 80: return 1
    if sys < 120 and dia < 80: return 0
    return 0

def temp_score(t: Any) -> int:
    try:
        v = float(t)
    except Exception:
        return 0
    if v <= 99.5: return 0
    if v <= 100.9: return 1
    return 2  # >= 101.0

def age_score(a: Any) -> int:
    try:
        v = int(a)
    except Exception:
        return 0
    if v < 40: return 0
    if v <= 65: return 1
    return 2

def total_score(p: dict) -> int:
    return bp_score(p.get("blood_pressure")) + temp_score(p.get("temperature")) + age_score(p.get("age"))

def has_bad_data(p: dict) -> bool:
    # invalid if any of bp/age/temp malformed or missing
    s = bp_score(p.get("blood_pressure"))
    t = temp_score(p.get("temperature"))
    a = age_score(p.get("age"))
    # re-validate by parsing to detect malformed values
    sys, dia = _parse_bp(p.get("blood_pressure"))
    bad_bp = sys is None or dia is None
    try: float(p.get("temperature")); bad_temp = False
    except: bad_temp = True
    try: int(p.get("age")); bad_age = False
    except: bad_age = True
    return bad_bp or bad_temp or bad_age

def is_fever(p: dict) -> bool:
    try: return float(p.get("temperature")) >= 99.6
    except: return False
