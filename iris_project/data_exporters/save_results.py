from __future__ import annotations

import pandas as pd

try:
    from mage_ai.data_preparation.decorators import data_exporter, test
except ImportError:
    def data_exporter(function):
        return function

    def test(function):
        return function


@data_exporter
def export(result: dict, *args, **kwargs) -> str:
    output_path = kwargs.get("output_path", "iris_predictions.csv")
    pd.DataFrame({
        "actual": result["actual"],
        "predicted": result["predictions"],
    }).to_csv(output_path, index=False)
    return output_path


@test
def test_output_shape(result: str, *args) -> None:
    assert result.endswith(".csv")

