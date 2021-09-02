from datetime import datetime

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from . import data


def test_get_wind_plant_coordinates():
    ds = xr.Dataset(
        {
            "longitude": ([1]),
            "latitude": ([2]),
        }
    )
    expected = (1, 2)

    result = data._get_wind_plant_coordinates(ds)

    assert result == expected


def test_get_grid_coordinates():
    df = pd.DataFrame(
        data=[[1, 2], [1, 2]],
        index=pd.MultiIndex.from_arrays(
            [
                [1.0, 2.0],
                [1.0, 2.0],
            ],
            names=["longitude", "latitude"],
        ),
    )
    expected = [1.0, 2.0]

    result = data._get_grid_coordinates(df, coordinate="longitude")

    assert result == expected


@pytest.mark.parametrize(
    ("grid", "coordinates", "expected"),
    [
        (
            [[3, 2, 1], [3, 2, 1]],
            (1.4, 1.4),
            (1, 1),
        ),
        (
            [[3, 1, 2], [3, 2, 1]],
            (1.6, 1.6),
            (2, 2),
        ),
        (
            [[1, 2, 3], [1, 2, 3]],
            (1.4, 1.6),
            (1, 2),
        ),
    ],
)
def test_get_closest_grid_point(grid, coordinates, expected):
    result = data._get_closest_grid_point(grid, coordinates=coordinates)

    assert result == expected


@pytest.mark.parametrize(
    ("coordinates", "value", "expected"),
    [
        (
            [1, 2, 3],
            1.4,
            1,
        ),
        (
            [10.0, 20.0, 30.0],
            16.0,
            20.0,
        ),
        (
            [30.0, 10.0, 20.0],
            16.0,
            20.0,
        ),
    ],
)
def test_get_closest_coordinate(coordinates, value, expected):
    result = data._get_closest_coordinate(coordinates, value=value)

    assert result == expected


def test_resample_production_data_to_hourly_timeseries():
    dates = pd.date_range(
        start=datetime(2020, 1, 1),
        end=datetime(2020, 1, 1, 1),
        freq="10min",
    )
    production_data = range(len(dates))
    average_first_hour = np.mean(production_data[:-1])
    average_second_hour = np.mean(production_data[-1:])
    production = pd.DataFrame(
        [[value] for value in production_data],
        columns=["production"],
        index=pd.MultiIndex.from_arrays(
            [list(range(len(dates))), dates], names=["longitude", "time"]
        ),
    )
    expected = pd.Series(
        data=[average_first_hour, average_second_hour],
        index=pd.DatetimeIndex(
            [datetime(2020, 1, 1), datetime(2020, 1, 1, 1)], name="time", freq="H"
        ),
        name="production",
    )

    result = data._resample_production_data_to_hourly_timeseries(production)

    pd.testing.assert_series_equal(result, expected)
