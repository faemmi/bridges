import pathlib
import sys
import mantik
import pytest
from sklearn.ensemble import GradientBoostingRegressor

__file_loc__ = pathlib.Path(__file__).parent
sys.path.append((__file_loc__ / "../payload").as_posix())

import algorithm
import utils


@pytest.fixture()
def time_of_day(dates):
    return [1 / (i + 1) for i, _ in enumerate(dates)]


@pytest.fixture()
def time_of_year(dates):
    return [1 / (i * 10 + 1) for i, _ in enumerate(dates)]


@pytest.fixture()
def bundle(dates, production, time_of_day, time_of_year):
    values = utils.convert_to_columns(dates, production, time_of_day, time_of_year)
    return mantik.types.Bundle(value=values)


@pytest.fixture()
def meta():
    return mantik.types.MetaVariables()


def test_train(bundle, meta):
    result = algorithm.train(bundle, meta)

    assert isinstance(result.value[0][0], float)


def test_try_init(bundle, meta):
    test_train(bundle, meta)

    result = algorithm.try_init()

    assert isinstance(result, GradientBoostingRegressor)


def test_apply(bundle, meta, dates, production):
    test_train(bundle, meta)

    model = algorithm.try_init()

    prediction = algorithm.apply(model, bundle)
    dates_prediction, power_prediction = utils.unpack_bundle(prediction)

    assert dates_prediction == dates
    assert all(round(left) == right for left, right in zip(power_prediction, production))
