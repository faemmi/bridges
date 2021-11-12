import typing as t

import pytest


@pytest.fixture()
def dates():
    return [
        "2017-01-01T00:00:00",
        "2017-01-01T00:10:00",
        "2017-01-01T00:20:00",
        "2017-01-01T00:30:00",
        "2017-01-01T00:40:00",
        "2017-01-01T00:50:00",
    ]


@pytest.fixture()
def production(dates) -> t.List[int]:
    return [value for value in range(len(dates))]
