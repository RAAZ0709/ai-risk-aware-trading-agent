import joblib
from src.data_loader import download_stock_data
from src.features import create_features
from src.model import FEATURE_COLUMNS
from src.risk_management import calculate_risk_levels


def predict_next_day(ticker: str = "AAPL"):
    model = joblib.load("model.joblib")

    stock_data = download_stock_data(ticker)
    featured_data = create_features(stock_data)

    latest_data = featured_data.iloc[[-1]]
    X_latest = latest_data[FEATURE_COLUMNS]

    prediction = model.predict(X_latest)[0]
    probabilities = model.predict_proba(X_latest)[0]

    confidence = max(probabilities) * 100

    direction = "UP" if prediction == 1 else "DOWN"
    risk_levels = calculate_risk_levels(
        entry_price=float(latest_data["Close"].iloc[0]),
        direction=direction,
)

    return {
        "ticker": ticker.upper(),
        "prediction": direction,
        "confidence": round(confidence, 2),
        "latest_close": round(float(latest_data["Close"].iloc[0]), 2),
        "stop_loss": risk_levels["stop_loss"],
        "take_profit": risk_levels["take_profit"],
        "risk_reward_ratio": risk_levels["risk_reward_ratio"],
    }



if __name__ == "__main__":
    result = predict_next_day("AAPL")

    print("\nNext-Day Prediction")
    print("-------------------")
    print(f"Stock: {result['ticker']}")
    print(f"Latest Close: ${result['latest_close']}")
    print(f"Predicted Direction: {result['prediction']}")
    print(f"Model Confidence: {result['confidence']}%")
    print(f"Suggested Stop-Loss: ${result['stop_loss']}")
    print(f"Suggested Take-Profit: ${result['take_profit']}")
    print(f"Risk-Reward Ratio: 1:{result['risk_reward_ratio']}")