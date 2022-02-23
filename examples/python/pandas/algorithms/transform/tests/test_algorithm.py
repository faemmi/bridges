import pathlib
import sys

import mantik

__file_loc__ = pathlib.Path(__file__).parent
sys.path.append((__file_loc__ / "../payload").as_posix())

import algorithm


def test_apply():
    bundle = mantik.types.Bundle(value=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    meta = mantik.types.MetaVariables()
    expected = [[6], [15], [24]]

    result = algorithm.apply(bundle, meta)

    assert isinstance(result, mantik.types.Bundle)
    assert result.value == expected
