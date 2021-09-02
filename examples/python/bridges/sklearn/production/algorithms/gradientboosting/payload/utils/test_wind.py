import pandas as pd

from . import wind


def test_calculate_wind_speed():
    u = pd.Series(data=[3.0, 3.0, 3.0])
    v = pd.Series(data=[4.0, 4.0, 4.0])
    expected = pd.Series(data=[5.0, 5.0, 5.0])

    result = wind.calculate_absolute_wind_speed(
        wind_speed_east=u,
        wind_speed_north=v,
    )

    pd.testing.assert_series_equal(result, expected)


def test_calculate_wind_direction_angle():
    u = pd.Series([10.0])
    v = pd.Series([10.0])
    expected = pd.Series([45.0])

    result = wind.calculate_wind_direction_angle(
        wind_speed_east=u,
        wind_speed_north=v,
    )

    pd.testing.assert_series_equal(result, expected)
