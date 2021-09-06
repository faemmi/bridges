from typing import Dict
from typing import Tuple

import numpy as np
import pandas as pd
import xarray as xr


def calculate_absolute_wind_speed_and_wind_direction(
    grid_point: Dict[str, float],
    model_level: int,
    model_level_data: xr.Dataset,
) -> Tuple[pd.Series, pd.Series]:
    """Calculate the absolute wind speed and wind direction.

    Parameters
    ----------
    grid_point : tuple[float, float]
        Grid point for which to calculate the wind properties.
    model_level : int
        Model level for which to calculate the wind properties.
    model_level_data : pandas.DataFrame
        Model level data from the `maelstrom-weather-model-level` dataset.


    Returns
    -------
    tuple[pandas.Series, pandas.Series]
        Absolute wind speed and wind direction (angle relative to longitude).

    """
    model_level_index = {**grid_point, "level": model_level}
    wind_speed_east = model_level_data.loc[model_level_index]["u"]
    wind_speed_north = model_level_data.loc[model_level_index]["v"]
    absolute_wind_speed = calculate_absolute_wind_speed(
        wind_speed_east,
        wind_speed_north,
    )
    wind_direction = calculate_wind_direction_angle(
        wind_speed_east=wind_speed_east,
        wind_speed_north=wind_speed_north,
    )
    return absolute_wind_speed, wind_direction


def calculate_absolute_wind_speed(
    wind_speed_east: pd.Series, wind_speed_north: pd.Series
) -> pd.Series:
    """Calculate the absolte wind speed.

    Parameters
    ----------
    wind_speed_east : pd.Series
        Wind speed in East direction.
    wind_speed_north : pd.Series
        Wind speed in North direction.

    Returns
    -------
    pandas.Series
        Absolute wind speed.

    """
    return np.sqrt(wind_speed_east ** 2 + wind_speed_north ** 2)


def calculate_wind_direction_angle(
    wind_speed_east: pd.Series, wind_speed_north: pd.Series
) -> pd.Series:
    """Calculate wind direction angle relative to longitude.

    Parameters
    ----------
    wind_speed_east : pd.Series
        Wind speed in East direction.
    wind_speed_north : pd.Series
        Wind speed in North direction.

    Returns
    -------
    pandas.Series
        Wind direction angle relative to longitude in degrees.

    """
    angle = _calculate_angle_to_equator(
        opposite=wind_speed_north, adjacent=wind_speed_east
    )
    return 90.0 - angle


def _calculate_angle_to_equator(opposite: pd.Series, adjacent: pd.Series) -> pd.Series:
    angle_in_rad = np.arctan(opposite / adjacent)
    return _rad_to_deg(angle_in_rad)


def _rad_to_deg(angle: pd.Series) -> pd.Series:
    return angle * 360.0 / (2 * np.pi)
