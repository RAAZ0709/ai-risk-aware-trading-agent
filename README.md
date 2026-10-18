
# AI Risk-Aware Trading Agent

An AI-based stock direction prediction system that uses historical market data and technical indicators to predict whether a stock may move UP or DOWN. It also calculates suggested stop-loss and take-profit levels to support risk-aware analysis.

## Features

- Stock direction prediction using Random Forest.
- Confidence score for model predictions.
- Technical indicators such as RSI, MACD, and moving averages.
- Suggested stop-loss and take-profit levels.
- Historical stock price chart.
- Interactive Streamlit dashboard.
- FastAPI backend with Swagger documentation.
- Automated tests using pytest.

## Technologies Used

- Python
- Pandas and NumPy
- Scikit-learn
- yfinance
- Technical Analysis (`ta`)
- Streamlit
- FastAPI
- Uvicorn
- Pytest


## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RAAZ0709/ai-risk-aware-trading-agent.git
cd ai-risk-aware-trading-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the Streamlit Dashboard

Open a terminal in the project folder and run:

```bash
streamlit run app.py
```

### 6. Start the FastAPI Backend

Open a second terminal, activate the virtual environment, and run:

```bash
uvicorn api:app --reload --port 8000
```

API documentation: http://127.0.0.1:8000/docs

## Running Tests

```bash
pytest -v
```

## Disclaimer

This project is for educational and research purposes only. Predictions are uncertain and should not be treated as financial advice or guarantees of profit.
