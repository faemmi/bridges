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
import pickle
import logging
from typing import List

import numpy as np
import xarray as xr

import mantik
import mantik.types
import utils

__my_loc__ = pathlib.Path("/opt")
# __my_loc__ = pathlib.Path("./../../../")
MODEL_FILE = "model.pickle"
MODEL_LEVEL = 133  # is roughly at the wind plant's hub height (100 m)

logger = logging.getLogger(__name__)


def train(bundle: mantik.types.Bundle, meta: mantik.types.MetaVariables) -> mantik.types.Bundle:
    logger.info("here")
    constants, production, ml, sfc = _open_train_files()

    closest_grid_point = utils.get_closest_grid_point_to_wind_plant(
        production_data=production,
        data=ml,
    )
    air_density = utils.calculate_air_density(
        grid_point=closest_grid_point,
        model_level=MODEL_LEVEL,
        model_level_data=ml,
        surface_data=sfc,
        constants=constants,
    )
    absolute_wind_speed, wind_direction = utils.calculate_absolute_wind_speed_and_wind_direction(
        grid_point=closest_grid_point,
        model_level=MODEL_LEVEL,
        model_level_data=ml,
    )
    dates = absolute_wind_speed.coords["time"].to_index().to_list()
    time_of_day, time_of_year = utils.get_time_of_day_and_year(dates)
    prod_resampled = utils.resample_and_clear_production_data_to_hourly_timeseries(
        production, dates=dates
    )
    model = utils.train_model(
        air_density=air_density,
        absolute_wind_speed=absolute_wind_speed,
        wind_direction=wind_direction,
        time_of_day=time_of_day,
        time_of_year=time_of_year,
        production=prod_resampled,
    )

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    score = utils.get_model_score(
        model,
        air_density=air_density,
        absolute_wind_speed=absolute_wind_speed,
        wind_direction=wind_direction,
        time_of_day=time_of_day,
        time_of_year=time_of_year,
        production=prod_resampled,
    )
    
    value = [[score]]
    return mantik.types.Bundle(value=value)


def _open_train_files():
    const = xr.open_dataset(__my_loc__ / "data/ECMWF_AB137.nc")
    production = xr.open_dataset(__my_loc__ / "data/wald9.nc")
    ml = xr.open_dataset(__my_loc__ / "data/ml_20190101_00.nc")
    sfc = xr.open_dataset(__my_loc__ / "data/sfc_20190101_00.nc")
    ml, sfc = _round_coords(ml, sfc)
    return const, production, ml, sfc


def _open_predict_files():
    ml = xr.open_dataset(__my_loc__ / "data/ml_20190103_00.nc")
    sfc = xr.open_dataset(__my_loc__ / "data/sfc_20190103_00.nc")
    ml, sfc = _round_coords(ml, sfc)
    return ml, sfc


def _round_coords(*datasets: List[xr.Dataset]) -> List[xr.Dataset]:
    for ds in datasets:
        for coord in ["longitude", "latitude"]:
            ds.coords[coord] = ds.coords[coord].round(1)
    return datasets


def try_init():
    with (open(MODEL_FILE, "rb")) as f:
        return pickle.load(f)


def apply(model, bundle: mantik.types.Bundle) -> mantik.types.Bundle:
    constants, production, _, _ = _open_train_files()
    ml, sfc = _open_predict_files()

    closest_grid_point = utils.get_closest_grid_point_to_wind_plant(
        production_data=production,
        data=ml,
    )
    air_density = utils.calculate_air_density(
        grid_point=closest_grid_point,
        model_level=MODEL_LEVEL,
        model_level_data=ml,
        surface_data=sfc,
        constants=constants,
    )
    absolute_wind_speed, wind_direction = utils.calculate_absolute_wind_speed_and_wind_direction(
        grid_point=closest_grid_point,
        model_level=MODEL_LEVEL,
        model_level_data=ml,
    )
    
    dates = absolute_wind_speed.coords["time"].to_index().to_list()
    time_of_day, time_of_year = utils.get_time_of_day_and_year(dates)
    production_forecast = utils.predict_power_production(
        model,
        air_density=air_density,
        absolute_wind_speed=absolute_wind_speed,
        wind_direction=wind_direction,
        time_of_day=time_of_day,
        time_of_year=time_of_year,
    )
    production_real = utils.resample_and_clear_production_data_to_hourly_timeseries(
        production, dates=dates
    )
    power_rating = utils.get_power_rating(production)
    nmae = utils.normalized_mean_absolute_error(
        production_real.values, 
        production_forecast.values, 
        normalization=power_rating,
    )
    times = [date.isoformat() for date in dates]

    value = list(list(row) for row in zip(times, production_forecast.values))
    return mantik.types.Bundle(value=value)


if __name__ == "__main__":
    train(None, None)
