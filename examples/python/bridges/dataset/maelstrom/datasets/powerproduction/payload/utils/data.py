import re
from datetime import datetime
from typing import Union
from typing import Tuple
from typing import Type
from typing import List
from typing import Dict

import numpy as np
import pandas as pd
import xarray as xr

Number = Type[Union[int, float]]


def get_closest_grid_point_to_wind_plant(
    production_data: xr.Dataset,
    data: xr.Dataset,
) -> Dict[str, float]:
    """Get the grid point in the data closest to the wind plant.

    Parameters
    ----------
    production_data : xarray.Datases
        Production data from the `maelstrom-power-production` dataset.
        Needs to be of type `xarray.Dataset` since its header contains
        the meta information with the wind plant's coordinates.
    data : pandas.DataFrame
        The data either from the `maelstrom-weather-model-level` or
        `maelstrom-weather-pressure-level` dataset. These contain the
        grid points.

    Returns
    -------
    dict[float, float]
        Grid point coordinates that are closest to the wind plant.

    """
    plant_coordinates = _get_wind_plant_coordinates(production_data)
    grid = [
        _get_grid_coordinates(data, "longitude"),
        _get_grid_coordinates(data, "latitude"),
    ]
    longitude, latitude = _get_closest_grid_point(grid, coordinates=plant_coordinates)
    return {"longitude": longitude, "latitude": latitude}


def _get_wind_plant_coordinates(ds: xr.Dataset) -> Tuple[Number, Number]:
    """Get the coordinates (longitude, latitude) of a wind plant from the production data.

    Parameters
    ----------
    ds : xarray.Dataset
        The production data from the dataset `maelstrom-power-production`.

    Returns
    -------
    tuple
        Longitude and latitude of the wind plant.

    """
    coordinates = ds.coords
    longitude = coordinates["longitude"].values[0]
    latitude = coordinates["latitude"].values[0]
    return longitude, latitude


def _get_grid_coordinates(ds: xr.Dataset, coordinate: str) -> np.array:
    """Get the unique coordinates (longitude and latitude) from a series.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with coordinates as index.
    coordinates : list[str], default ["longitude", "latitude"]
        The coordinates to get as a dataframe.

    Returns
    -------
    pandas.Series
        Contains the unique coordinates as columns.

    """
    return [round(float(val), 1) for val in ds.coords[coordinate].values]


def _get_closest_grid_point(
    grid: List[np.array], coordinates: Tuple[Number, Number]
) -> Tuple[Number, Number]:
    """Get the grid point that is closest to the given coordinates.

    Parameters
    ----------
    grid : list[list, list]
        List with two lists, each representing coordinates.
        For each coordinate, the value closest to the respective value at
        the same column of the tuple will be returned.
    coordinates : tuple
        Coordinates whose closest grid point to get from `grid`.
        The first value will find the closest value in the first column
        of `coordinates`, the second value that in the second column.

    Returns
    -------
    tuple
        The closest values in each column of `grid`.

    """
    closest_values = (
        _get_closest_coordinate(
            axis,
            value=coordinates[index],
        )
        for index, axis in enumerate(grid)
    )
    return tuple(closest_values)


def _get_closest_coordinate(coordinates: np.array, value: Number) -> Number:
    exactmatch = [coordinate for coordinate in coordinates if coordinate == value]
    if exactmatch:
        [match] = exactmatch
        return match
    return min(coordinates, key=lambda x: abs(x - value))


def resample_and_clear_production_data_to_hourly_timeseries(
    production_data: xr.Dataset,
    dates: List[datetime],
) -> xr.DataArray:
    """Resample the production data to an hourly timeseries and clear negative values.

    Parameters
    ----------
    production_data : pandas.DataFrame
        Production data from the `maelstrom-power-production` dataset.
    dates : list[datetime]
        Dates from the weather data to get all matching timestamps of the resample.

    Returns
    -------
    pandas.Series
        Production data resampled to an hourly time series.
        The data are averaged (mean) over the time windows.
        Negative values are set to 0.

    """
    resampled = _resample_production_data_to_hourly_timeseries(production_data.to_dataframe())
    resampled_and_matching_dates = resampled.loc[dates]
    resampled_and_matching_dates[resampled_and_matching_dates < 0.0] = 0.0
    return resampled_and_matching_dates.to_xarray()


def _resample_production_data_to_hourly_timeseries(
    production: pd.DataFrame,
    time_index_name: str = "time",
    production_column_name: str = "production",
) -> pd.Series:
    """Resample the production data to an hourly timeseries."""
    production_copy = production.copy()
    production_copy.reset_index(inplace=True)
    production_copy = production_copy.set_index(time_index_name)
    return production_copy[production_column_name].resample("1h").mean()


def get_power_rating(data: xr.Dataset) -> float:
    """Get the power rating of a wind plant."""
    power_rating_header = data.attrs["power rating"]
    match = re.search(r"[0-9]*", power_rating_header)
    power_rating = float(match[0])
    return power_rating
