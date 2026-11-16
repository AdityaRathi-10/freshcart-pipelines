from __future__ import annotations

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(function):
        return function

    def test(function):
        return function


@transformer
def transform(df: pd.DataFrame, *args, **kwargs) -> dict:
    max_depth = int(kwargs.get("max_depth", 3))
    train = df[df["split"] == "train"]
    test_data = df[df["split"] == "test"]
    features = [column for column in df.columns if column not in {"target", "split"}]
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(train[features], train["target"])
    accuracy = float(model.score(test_data[features], test_data["target"]))
    predictions = model.predict(test_data[features])
    return {
        "model": model,
        "features": features,
        "predictions": predictions,
        "actual": test_data["target"].to_numpy(),
        "test_accuracy": accuracy,
        "max_depth": max_depth,
    }


@test
def test_accuracy(result: dict, *args) -> None:
    assert 0.0 <= result["test_accuracy"] <= 1.0
    assert result["test_accuracy"] >= 0.80

