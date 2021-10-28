import typing as t

import numpy as np
import xarray as xr


def get_dates_as_strings(data: xr.Dataset) -> t.List[str]:
    dates = data.coords["time"].values
    return [np.datetime_as_string(date, unit="s") for date in dates]


def convert_to_columns(*columns):
    lengths = set(list(len(column) for column in columns))
    if len(lengths) != 1:
        raise ValueError("Input objects must have equal length")
    return [[*column] for column in zip(*columns)]
