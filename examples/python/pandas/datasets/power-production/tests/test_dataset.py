import pathlib
import sys

import mantik
import pytest

__file_loc__ = pathlib.Path(__file__).parent
sys.path.append((__file_loc__ / "../payload").as_posix())

import dataset


@pytest.mark.parametrize("runs_in_docker", [True, False])
def test_get(dates, production, runs_in_docker):
    meta = mantik.types.MetaVariables(
        runs_in_docker=mantik.types.MetaVariable(
            name="runs_in_docker", bundle=mantik.types.Bundle(value=runs_in_docker)
        )
    )
    expected_dates = [date.isoformat() for date in dates]
    expected = [[date, prod] for date, prod in zip(expected_dates, production)]

    result = dataset.get(meta)

    assert isinstance(result, mantik.types.Bundle)
    assert result.value == expected
