import dataclasses

import climetlab as cml
import dataset
import mantik.types
import xarray as xr


@dataclasses.dataclass
class DataSet:
    data: xr.Dataset

    def to_xarray(self) -> xr.Dataset:
        return self.data


def test_get(monkeypatch, dates, production, production_xarray):
    monkeypatch.setattr(cml, "load_dataset", lambda *args, **kwargs: DataSet(production_xarray))
    meta = mantik.types.MetaVariables(
        wind_plant_id=mantik.types.MetaVariable(
            name="wind_plant_id", bundle=mantik.types.Bundle(value="test_id")
        )
    )
    expected_dates = [date.isoformat() for date in dates]
    expected = [[date, prod] for date, prod in zip(expected_dates, production)]

    result = dataset.get(meta)

    assert isinstance(result, mantik.types.Bundle)
    assert result.value == expected
