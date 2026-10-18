def calculate_risk_levels(
    entry_price: float,
    direction: str,
    stop_loss_pct: float = 2.0,
    take_profit_pct: float = 4.0,
):
    """Calculate suggested stop-loss and take-profit prices."""

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero.")

    if not 0 < stop_loss_pct < 100:
        raise ValueError("Stop-loss percentage must be between 0 and 100.")

    if not 0 < take_profit_pct < 100:
        raise ValueError("Take-profit percentage must be between 0 and 100.")

    direction = direction.upper()

    if direction == "UP":
        stop_loss = entry_price * (1 - stop_loss_pct / 100)
        take_profit = entry_price * (1 + take_profit_pct / 100)

    elif direction == "DOWN":
        stop_loss = entry_price * (1 + stop_loss_pct / 100)
        take_profit = entry_price * (1 - take_profit_pct / 100)

    else:
        raise ValueError("Direction must be UP or DOWN.")

    return {
        "entry_price": round(entry_price, 2),
        "direction": direction,
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_reward_ratio": round(
            take_profit_pct / stop_loss_pct, 2
        ),
    }


if __name__ == "__main__":
    levels = calculate_risk_levels(
        entry_price=342.00,
        direction="UP",
    )

    print("Risk Management")
    print("----------------")
    print(f"Entry Price: ${levels['entry_price']}")
    print(f"Direction: {levels['direction']}")
    print(f"Suggested Stop-Loss: ${levels['stop_loss']}")
    print(f"Suggested Take-Profit: ${levels['take_profit']}")
    print(f"Risk-Reward Ratio: 1:{levels['risk_reward_ratio']}")