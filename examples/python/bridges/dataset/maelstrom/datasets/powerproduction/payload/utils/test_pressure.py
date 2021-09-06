import pandas as pd
import pytest

from . import pressure


@pytest.mark.parametrize(
    ("p_s", "A_k", "B_k", "expected"),
    [
        (1.0, pd.Series([1.0, 1.0]), pd.Series([1.0, 1.0]), pd.Series([2.0, 2.0])),
        (2.0, pd.Series([1.0, 1.0]), pd.Series([2.0, 2.0]), pd.Series([5.0, 5.0])),
    ],
)
def test_calculate_pressure_levels(p_s, A_k, B_k, expected):
    result = pressure._calculate_pressure_levels(
        p_s=p_s,
        A_k=A_k,
        B_k=B_k,
    )

    pd.testing.assert_series_equal(result, expected)
