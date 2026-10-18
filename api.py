
from fastapi import FastAPI, HTTPException, Query
from src.predict import predict_next_day

app = FastAPI(
    title="AI Risk-Aware Trading Agent API",
    description="Stock direction prediction and risk-management API",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "AI Risk-Aware Trading Agent API is running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/predict/{ticker}")
def predict_stock(
    ticker: str,
):
    try:
        return predict_next_day(ticker)
    except (ValueError, KeyError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check the ticker and data source.",
        )
