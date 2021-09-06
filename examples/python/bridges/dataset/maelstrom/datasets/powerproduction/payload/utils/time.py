from datetime import datetime
from typing import List
from typing import Tuple

import pandas as pd


def get_time_of_day_and_year(dates: List[datetime]) -> Tuple[pd.Series, pd.Series]:
    """Calculate the time of day and year for given datetimes."""
    time_of_day = get_time_of_day(dates)
    time_of_year = get_time_of_year(dates)
    return time_of_day, time_of_year


def get_time_of_day(dates: List[datetime]) -> pd.Series:
    """Calculate relative time of day for datetimes."""
    data = [_time_of_day(date) for date in dates]
    return pd.Series(
        data,
        index=dates,
        name="time_of_day",
    )


def get_time_of_year(dates: List[datetime]) -> pd.Series:
    """Calculate relative time of year for datetimes."""
    data = [_time_of_year(date) for date in dates]
    return pd.Series(
        data,
        index=dates,
        name="time_of_day",
    )


def _time_of_day(dt: datetime) -> float:
    """Convert a given datetime `dt` to a point on the unit circle, where the 'period' corresponds to one day.

    :param datetime.datetime dt: input datetime UTC
    :returns: `float` between 0 and 1 corresponding to the phase
    """
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (dt - midnight).total_seconds()
    return seconds_since_midnight / 86400


def _time_of_year(dt: datetime) -> float:
    """Convert a given datetime `dt` to a point on the unit circle, where the 'period' corresponds to one year.

    :param datetime.datetime dt: input datetime (preferably UTC)
    :returns: `float` between 0 and 1 corresponding to the phase

    This function makes a small mistake in leap years as it considers the length of the year to be 365d always.
    """
    # Convert to UTC before
    return (dt.timetuple().tm_yday - 1) / 365
