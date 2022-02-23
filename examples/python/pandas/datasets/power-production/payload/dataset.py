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
import pathlib

import mantik
import numpy as np
import pandas as pd
import utils

__file_loc__ = pathlib.Path(__file__).parent


def get(meta: mantik.types.MetaVariables) -> mantik.types.Bundle:
    runs_in_docker = meta.get("runs_in_docker")
    if runs_in_docker:
        df = _load_data_from_payload()
    else:
        df = _load_data_from_file_system()

    dates = utils.get_dates_as_strings(df)
    production = _get_production_values(df)

    result = utils.convert_to_columns(dates[:10], production[:10])

    return mantik.types.Bundle(value=result)


def _load_data_from_file_system() -> pd.DataFrame:
    return pd.read_csv("/home/fabian/Documents/mantik/test-data.csv")


def _load_data_from_payload() -> pd.DataFrame:
    return pd.read_csv(__file_loc__ / "test-data.csv")


def _get_production_values(data: pd.DataFrame) -> np.ndarray:
    return data["production"].values.astype(float).flatten()
