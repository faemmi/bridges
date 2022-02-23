import datetime
import typing as t

import numpy as np
import pandas as pd
import pytest


@pytest.fixture()
def dates():
    return pd.date_range(
        start=datetime.datetime(2000, 1, 1),
        end=datetime.datetime(2000, 1, 1, 9),
        freq="1h",
    )


@pytest.fixture()
def production(dates) -> t.List[int]:
    return [np.float32(index + 1) * 100 for index, _ in enumerate(dates)]


@pytest.fixture()
def production_df(dates, production):
    dates_isoformatted = [date.isoformat() for date in dates]
    return pd.DataFrame(
        data=zip(dates_isoformatted, production),
        columns=["date", "production"],
    )
