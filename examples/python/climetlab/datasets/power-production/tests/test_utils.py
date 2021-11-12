import pathlib
import sys

__file_loc__ = pathlib.Path(__file__).parent
sys.path.append((__file_loc__ / "../payload").as_posix())

import utils


def test_get_dates_as_string(dates, production_xarray):
    expected = [date.isoformat() for date in dates]

    result = utils.get_dates_as_strings(production_xarray)

    assert result == expected
