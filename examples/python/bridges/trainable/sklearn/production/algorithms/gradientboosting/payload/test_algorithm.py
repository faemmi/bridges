import mantik.types

import algorithm


def test_train():
    result = algorithm.train(None, None)
    
    assert isinstance(result, mantik.types.Bundle)
    assert isinstance(result.value, list)
    assert isinstance(result.value[0], list)

def test_apply():
    model = algorithm.try_init()
    result = algorithm.apply(model, None)
    
    assert isinstance(result, mantik.types.Bundle)
    assert isinstance(result.value, list)
    assert isinstance(result.value[0], tuple)
