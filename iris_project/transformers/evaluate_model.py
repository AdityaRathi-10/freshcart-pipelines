from __future__ import annotations

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(function):
        return function

    def test(function):
        return function


@transformer
def transform(result: dict, *args, **kwargs) -> dict:
    labels = sorted(set(result["actual"]) | set(result["predictions"]))
    matrix = confusion_matrix(result["actual"], result["predictions"], labels=labels)
    metrics = pd.DataFrame(classification_report(
        result["actual"], result["predictions"], output_dict=True, zero_division=0
    )).transpose()
    return {"confusion_matrix": matrix, "labels": labels, "metrics": metrics}


@test
def test_metrics_exist(result: dict, *args) -> None:
    assert result["confusion_matrix"].shape == (3, 3)
    assert not result["metrics"].empty

