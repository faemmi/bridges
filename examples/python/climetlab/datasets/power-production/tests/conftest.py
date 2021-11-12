import datetime
import typing as t

import numpy as np
import pandas as pd
import pytest
import xarray as xr


@pytest.fixture()
def dates():
    return pd.date_range(
        start=datetime.datetime(2020, 1, 1),
        end=datetime.datetime(2020, 1, 1, 1),
        freq="10min",
    )


@pytest.fixture()
def production(dates) -> t.List[int]:
    return [np.float32(value) for value in range(len(dates))]


@pytest.fixture()
def production_xarray(dates, production):
    return xr.Dataset(
        data_vars={
            "production": ("time", production),
        },
        coords={
            "time": dates,
        },
    )
