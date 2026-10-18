
import pytest
from src.risk_management import calculate_risk_levels


def test_up_prediction_risk_levels():
    result = calculate_risk_levels(100, "UP")

    assert result["stop_loss"] == 98.0
    assert result["take_profit"] == 104.0
    assert result["risk_reward_ratio"] == 2.0


def test_down_prediction_risk_levels():
    result = calculate_risk_levels(100, "DOWN")

    assert result["stop_loss"] == 102.0
    assert result["take_profit"] == 96.0
    assert result["risk_reward_ratio"] == 2.0


def test_invalid_entry_price():
    with pytest.raises(ValueError):
        calculate_risk_levels(0, "UP")


def test_invalid_direction():
    with pytest.raises(ValueError):
        calculate_risk_levels(100, "SIDEWAYS")


def test_invalid_stop_loss_percentage():
    with pytest.raises(ValueError):
        calculate_risk_levels(
            100, "UP", stop_loss_pct=0
        )
