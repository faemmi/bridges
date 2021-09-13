import algorithm
import mantik.types


def test_apply():
    value = [[6], [15], [24]]
    bundle = mantik.types.Bundle(value=value)
    meta = mantik.types.MetaVariables()
    expected = [[6 ** 2], [15 ** 2], [24 ** 2]]

    result = algorithm.apply(bundle, meta)

    assert isinstance(result, mantik.types.Bundle)
    assert result.value == expected
