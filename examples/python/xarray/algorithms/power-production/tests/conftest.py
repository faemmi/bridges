import datetime
import typing as t

import numpy as np
import pandas as pd
import pytest


@pytest.fixture()
def datetimes():
    return pd.date_range(
        start=datetime.datetime(2020, 1, 1),
        end=datetime.datetime(2020, 1, 1, 1),
        freq="10min",
    )


@pytest.fixture()
def dates(datetimes):
    return [date.isoformat() for date in datetimes]


@pytest.fixture()
def production(dates) -> t.List[int]:
    return [np.float32(value) for value in range(len(dates))]
