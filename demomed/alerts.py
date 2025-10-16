from typing import List, Dict
from .scoring import total_score, is_fever, has_bad_data

def build_alert_lists(patients: List[Dict]) -> dict:
    high = []
    fever = []
    bad = []
    for p in patients:
        pid = p.get("patient_id")
        if total_score(p) >= 4:
            high.append(pid)
        if is_fever(p):
            fever.append(pid)
        if has_bad_data(p):
            bad.append(pid)
    return {
        "high_risk_patients": high,
        "fever_patients": fever,
        "data_quality_issues": bad
    }
