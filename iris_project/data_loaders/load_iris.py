from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_iris

try:
    from mage_ai.data_preparation.decorators import data_loader, test
except ImportError:
    def data_loader(function):
        return function

    def test(function):
        return function


@data_loader
def load_data(*args, **kwargs) -> pd.DataFrame:
    return load_iris(as_frame=True).frame


@test
def test_shape(result: pd.DataFrame, *args) -> None:
    assert result.shape == (150, 5)

