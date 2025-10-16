from demomed.alerts import build_alert_lists

def test_alert_lists():
    pts = [
        {"patient_id":"A", "blood_pressure":"145/92","temperature":101.2,"age":70}, # high + fever
        {"patient_id":"B", "blood_pressure":"120/70","temperature":99.7,"age":30},  # fever only
        {"patient_id":"C", "blood_pressure":"bad","temperature":"ERR","age":"??"},   # data issue
    ]
    payload = build_alert_lists(pts)
    assert "A" in payload["high_risk_patients"]
    assert "A" in payload["fever_patients"] and "B" in payload["fever_patients"]
    assert "C" in payload["data_quality_issues"]
