
import yfinance as yf


def download_stock_data(
    ticker: str = "AAPL",
    period: str = "5y",
    interval: str = "1d",
):
    """Download historical stock market data."""
    if not ticker or not ticker.strip():
        raise ValueError("Ticker cannot be empty.")

    data = yf.download(
        ticker.strip().upper(),
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    # Handle MultiIndex columns returned by some yfinance versions.
    if getattr(data.columns, "nlevels", 1) > 1:
        data.columns = data.columns.get_level_values(0)

    required_columns = ["Open", "High", "Low", "Close", "Volume"]

    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    data = data[required_columns].copy()
    data = data.dropna(
        subset=["Open", "High", "Low", "Close"]
    )

    return data


if __name__ == "__main__":
    df = download_stock_data("AAPL")

    print(df.tail())
    print(f"\nTotal rows downloaded: {len(df)}")
    print(f"Columns: {list(df.columns)}")
