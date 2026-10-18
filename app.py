
import streamlit as st
import requests
from src.data_loader import download_stock_data

st.set_page_config(
    page_title="AI Trading Agent",
    page_icon="📈",
    layout="centered",
)

st.title("📈 AI Risk-Aware Trading Agent")
st.write("Predict stock direction and view suggested risk levels.")

ticker = st.text_input(
    "Enter stock ticker",
    value="AAPL",
    max_chars=15,
).strip().upper()

if st.button("Analyze Stock"):
    if not ticker:
        st.error("Please enter a valid stock ticker.")
    else:
        try:
            with st.spinner(f"Analyzing {ticker}..."):
                response = requests.get(
                    f"http://127.0.0.1:8000/predict/{ticker}",
                    timeout=60,
                )
                response.raise_for_status()
                result = response.json()

            st.subheader(f"Results for {result['ticker']}")
            st.subheader("Historical Stock Price")

            with st.spinner("Loading historical prices..."):
                price_data = download_stock_data(ticker, period="6mo")

            st.line_chart(price_data["Close"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Latest Close",
                    f"${result['latest_close']:.2f}",
                )
                st.metric(
                    "Predicted Direction",
                    result["prediction"],
                )

            with col2:
                st.metric(
                    "Model Confidence",
                    f"{result['confidence']:.2f}%",
                )
                st.metric(
                    "Risk-Reward Ratio",
                    f"1:{result['risk_reward_ratio']:.2f}",
                )

            st.subheader("Risk Management")

            col3, col4 = st.columns(2)

            with col3:
                st.metric(
                    "Suggested Stop-Loss",
                    f"${result['stop_loss']:.2f}",
                )

            with col4:
                st.metric(
                    "Suggested Take-Profit",
                    f"${result['take_profit']:.2f}",
                )

            st.warning(
                "Model predictions are uncertain and are not "
                "guarantees of future prices or profits."
            )

        except requests.exceptions.HTTPError as error:
            try:
                message = error.response.json().get(
                    "detail", "Stock analysis failed."
                )
            except ValueError:
                message = "Stock analysis failed."
            st.error(message)

        except requests.exceptions.RequestException:
            st.error(
                "Cannot connect to the API. "
                "Make sure the FastAPI server is running."
            )

        except Exception as error:
            st.error(f"Unable to analyze this stock: {error}")