import mantik.types

import algorithm


def test_apply():
    meta = {}
    result = algorithm.apply(meta)
    breakpoint()
    
    assert isinstance(result, mantik.types.Bundle)
    assert isinstance(result.value, list)
    assert isinstance(result.value[0], tuple)
