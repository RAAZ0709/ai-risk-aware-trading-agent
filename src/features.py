
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD


def create_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create technical indicators and a next-day direction target."""
    df = data.copy()

    close = df["Close"].astype(float)
    volume = df["Volume"].astype(float)

    # Price movement features
    df["Return_1d"] = close.pct_change()
    df["Return_5d"] = close.pct_change(5)

    # Moving averages
    df["SMA_10"] = close.rolling(window=10).mean()
    df["SMA_20"] = close.rolling(window=20).mean()
    df["SMA_50"] = close.rolling(window=50).mean()

    # Technical indicators
    df["RSI_14"] = RSIIndicator(
        close=close, window=14
    ).rsi()

    macd = MACD(close=close)
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()

    # Volume movement
    df["Volume_Change"] = volume.pct_change()

    # Target: 1 if the next closing price is higher, otherwise 0.
    next_close = close.shift(-1)
    df["Target"] = (next_close > close).astype("Int64").where(next_close.notna())

    # Remove rows with unavailable indicators and the final row,
    # whose next-day closing price is not yet known.
    df = df.replace([float("inf"), float("-inf")], float("nan"))
    df = df.dropna()

    print("Target distribution:")
    print(df["Target"].value_counts())

    return df


if __name__ == "__main__":
    from src.data_loader import download_stock_data

    stock_data = download_stock_data("AAPL")
    featured_data = create_features(stock_data)

    print(featured_data.tail())
    print(f"\nRows after feature engineering: {len(featured_data)}")
    print(f"Features and target: {list(featured_data.columns)}")
