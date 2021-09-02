from datetime import datetime

import pytest

from . import time


@pytest.mark.parametrize(
    ("dt", "expected"),
    [
        (datetime(2020, 1, 1), 0.0),
        (datetime(2020, 1, 1, 6), 0.25),
        (datetime(2020, 1, 1, 12), 0.5),
        (datetime(2020, 1, 1, 18), 0.75),
        (datetime(2020, 1, 2), 0.0),
    ],
)
def test_time_of_day(dt, expected):
    result = time._time_of_day(dt)

    assert result == expected


@pytest.mark.parametrize(
    ("dt", "expected"),
    [
        (datetime(2020, 1, 1), 0.0),
        (datetime(2020, 7, 2), 0.5),
        (datetime(2020, 12, 31), 1.0),
    ],
)
def test_time_of_year(dt, expected):
    result = time._time_of_year(dt)
    result_rounded = round(result, 2)

    assert result_rounded == expected
