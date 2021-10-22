import typing as t

import numpy as np
import xarray as xr


def get_dates_as_strings(data: xr.Dataset) -> t.List[str]:
    dates = data.coords["time"].values
    return [np.datetime_as_string(date, unit="s") for date in dates]
