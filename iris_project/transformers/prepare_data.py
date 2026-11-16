"""Split Iris data deterministically for the Mage pipeline and CI."""

from __future__ import annotations

import pandas as pd

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:  # Allows pytest to import this block outside Mage.
    def transformer(function):
        return function

    def test(function):
        return function


@transformer
def transform(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Iris input cannot be empty")
    result = df.copy()
    result["split"] = ["train" if index % 5 else "test" for index in range(len(result))]
    return result


@test
def test_split_is_80_20(result: pd.DataFrame, *args) -> None:
    assert (result["split"] == "train").sum() == 120
    assert (result["split"] == "test").sum() == 30

