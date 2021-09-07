import pandas as pd
import pytest

from mantik import types
import algorithm


def test_apply():
    bundle = types.Bundle(value=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    meta = types.MetaVariables()
    expected = [[6], [15], [24]]

    result_bundle = algorithm.apply(bundle, meta)
    result = result_bundle.value

    assert result == expected

