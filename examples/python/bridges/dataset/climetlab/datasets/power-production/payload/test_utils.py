import utils


def test_get_dates_as_string(dates, production_xarray):
    expected = [date.isoformat() for date in dates]

    result = utils.get_dates_as_strings(production_xarray)

    assert result == expected
