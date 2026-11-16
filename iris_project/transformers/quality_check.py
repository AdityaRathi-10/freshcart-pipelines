from __future__ import annotations

import pandas as pd

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(function):
        return function

    def test(function):
        return function


@transformer
def transform(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
    if df.isna().any().any():
        raise ValueError("Input contains missing values")
    if df["target"].nunique() != 3:
        raise ValueError("Expected exactly three Iris classes")
    return df


@test
def test_quality(result: pd.DataFrame, *args) -> None:
    assert not result.isna().any().any()
    assert result["target"].nunique() == 3

