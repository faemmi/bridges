import typing as t
from datetime import datetime


def convert_isoformat_dates_to_datetime(dates: t.List[str]) -> t.List[datetime]:
    return [datetime.fromisoformat(date) for date in dates]


def get_time_of_day_and_year(dates: t.List[datetime]) -> t.Tuple[t.List[float], t.List[float]]:
    """Calculate the time of day and year for given datetimes."""
    time_of_day = get_time_of_day(dates)
    time_of_year = get_time_of_year(dates)
    return time_of_day, time_of_year


def get_time_of_day(dates: t.List[datetime]) -> t.List[float]:
    """Calculate relative time of day for datetimes."""
    return [_time_of_day(date) for date in dates]


def get_time_of_year(dates: t.List[datetime]) -> t.List[float]:
    """Calculate relative time of year for datetimes."""
    return [_time_of_year(date) for date in dates]


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
