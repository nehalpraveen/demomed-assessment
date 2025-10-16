from demomed.scoring import bp_score, temp_score, age_score, total_score

def test_bp():
    assert bp_score("119/79") == 0
    assert bp_score("125/75") == 1
    assert bp_score("130/70") == 2
    assert bp_score("118/85") == 2
    assert bp_score("145/80") == 3
    assert bp_score("bad") == 0

def test_temp():
    assert temp_score(98.6) == 0
    assert temp_score(100.5) == 1
    assert temp_score(101.0) == 2
    assert temp_score("TEMP_ERROR") == 0

def test_age():
    assert age_score(25) == 0
    assert age_score(40) == 1
    assert age_score(65) == 1
    assert age_score(80) == 2
    assert age_score("fifty") == 0

def test_total():
    p = {"blood_pressure":"140/90","temperature":101.1,"age":70}
    assert total_score(p) == 3+2+2
