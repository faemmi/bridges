import pandas as pd

from . import density


def test_calculate_density():
    temperature = pd.Series(data=[1, 2, 3])
    pressure = pd.Series(data=[1, 2, 3])
    relative_humidity = pd.Series(data=[1, 2, 3])
    specific_humidity = pd.Series(data=[1, 2, 3])

    result = density._calculate_density(
        temperature=temperature,
        pressure=pressure,
        relative_humidity=relative_humidity,
        specific_humidity=specific_humidity,
    )

    assert isinstance(result, pd.Series)
