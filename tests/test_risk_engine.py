import pytest
from services.risk_engine import calculate_risk

def test_calculate_risk_low():
    result = calculate_risk(1, 1)
    assert result['score'] == 1
    assert result['level'] == 'Low'

def test_calculate_risk_medium():
    result = calculate_risk(2, 3)
    assert result['score'] == 6
    assert result['level'] == 'Medium'

def test_calculate_risk_high():
    result = calculate_risk(4, 3)
    assert result['score'] == 12
    assert result['level'] == 'High'

def test_calculate_risk_critical():
    result = calculate_risk(5, 5)
    assert result['score'] == 25
    assert result['level'] == 'Critical'

def test_calculate_risk_invalid_input_type():
    with pytest.raises(ValueError):
        calculate_risk("a", 2)

def test_calculate_risk_out_of_range():
    with pytest.raises(ValueError):
        calculate_risk(6, 3)
    with pytest.raises(ValueError):
        calculate_risk(0, 3)
