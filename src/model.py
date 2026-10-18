
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
)


FEATURE_COLUMNS = [
    "Return_1d",
    "Return_5d",
    "RSI_14",
    "MACD",
    "MACD_Signal",
    "Volume_Change",
]

def train_model(data: pd.DataFrame):
    """Train and evaluate a Random Forest using chronological data."""
    df = data.dropna(
        subset=FEATURE_COLUMNS + ["Target"]
    ).copy()

    if len(df) < 100:
        raise ValueError(
            "Not enough rows to train and evaluate the model."
        )

    # Keep time order: earlier data for training, later data for testing.
    split_index = int(len(df) * 0.8)

    X = df[FEATURE_COLUMNS]
    y = df["Target"].astype(int)

    print("Target distribution in model:")
    print(y.value_counts())

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    results = {
        "accuracy": accuracy_score(y_test, predictions),
        "report": classification_report(
            y_test,
            predictions,
            zero_division=0,
        ),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
    }

    return model, results


if __name__ == "__main__":
    from src.data_loader import download_stock_data
    from src.features import create_features

    stock_data = download_stock_data("AAPL")
    featured_data = create_features(stock_data)

    model, results = train_model(featured_data)

    joblib.dump(model, "model.joblib")
    print("Model saved successfully!")

    print(f"Training rows: {results['train_rows']}")
    print(f"Testing rows: {results['test_rows']}")
    print(f"Test accuracy: {results['accuracy']:.2%}")
    print("\nClassification report:")
    print(results["report"])
