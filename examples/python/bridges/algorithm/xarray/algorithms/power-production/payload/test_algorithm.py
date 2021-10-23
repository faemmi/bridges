import algorithm
import mantik
import utils


def test_apply(dates, production):
    values = utils.convert_to_columns(dates, production)
    bundle = mantik.types.Bundle(value=values)
    meta = mantik.types.MetaVariables()

    datetimes = utils.convert_isoformat_dates_to_datetime(dates)
    time_of_day = utils.get_time_of_day(datetimes)
    time_of_year = utils.get_time_of_year(datetimes)

    expected = utils.convert_to_columns(dates, production, time_of_day, time_of_year)

    result = algorithm.apply(bundle, meta)

    assert isinstance(result, mantik.types.Bundle)
    assert result.value == expected
