import mantik.types

import dataset


def test_apply():
    meta = mantik.types.MetaVariables()
    expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    result = dataset.get(meta)

    assert isinstance(result, mantik.types.Bundle)
    assert result.value == expected
