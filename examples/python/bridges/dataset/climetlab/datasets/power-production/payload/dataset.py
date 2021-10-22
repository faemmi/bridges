#
# This file is part of the Mantik Project.
# Copyright (c) 2020-2021 Mantik UG (Haftungsbeschränkt)
# Authors: See AUTHORS file
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.
#
# Additionally, the following linking exception is granted:
#
# If you modify this Program, or any covered work, by linking or
# combining it with other code, such other code is not for that reason
# alone subject to any of the requirements of the GNU Affero GPL
# version 3.
#
# You can be released from the requirements of the license by purchasing
# a commercial license.
#
import climetlab as cml
import mantik
import numpy as np
import utils
import xarray as xr


def get(meta: mantik.types.MetaVariables) -> mantik.types.Bundle:
    wind_plant_id = meta.get("wind_plant_id")
    dataset = _load_dataset(wind_plant_id)

    dates = utils.get_dates_as_strings(dataset)
    production = _get_production_values(dataset)

    result = _convert_to_columns(dates, production)

    return mantik.types.Bundle(value=result)


def _load_dataset(wind_plant_id: str) -> xr.Dataset:
    source = cml.load_dataset("maelstrom-power-production", wind_plant_id=wind_plant_id)
    return source.to_xarray()


def _get_production_values(data: xr.Dataset) -> np.ndarray:
    return data["production"].values.astype(float).flatten()


def _convert_to_columns(*columns):
    lengths = set(list(len(column) for column in columns))
    if len(lengths) != 1:
        raise ValueError("Input objects must have equal length")
    return [[*column] for column in zip(*columns)]
