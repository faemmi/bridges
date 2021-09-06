import pandas as pd
import xarray as xr
from sklearn.ensemble import GradientBoostingRegressor


def train_model(
    air_density: xr.DataArray,
    absolute_wind_speed: xr.DataArray,
    wind_direction: xr.DataArray,
    time_of_day: xr.DataArray,
    time_of_year: xr.DataArray,
    production: xr.DataArray,
) -> GradientBoostingRegressor:
    """Train the model with the given features and production data.

    All given data must be of the same shape.

    """
    x = _prepare_x_values(
        air_density.values,
        absolute_wind_speed.values,
        wind_direction.values,
        time_of_day.values,
        time_of_year.values,
    )
    y = production.values
    return GradientBoostingRegressor().fit(x, y)


def get_model_score(
    model: GradientBoostingRegressor,
    air_density: xr.DataArray,
    absolute_wind_speed: xr.DataArray,
    wind_direction: xr.DataArray,
    time_of_day: xr.DataArray,
    time_of_year: xr.DataArray,
    production: xr.DataArray,
) -> float:
    """Get the score of the model."""
    x = _prepare_x_values(
        air_density.values,
        absolute_wind_speed.values,
        wind_direction.values,
        time_of_day.values,
        time_of_year.values,
    )
    y = production.values
    return model.score(x, y)


def predict_power_production(
    model: GradientBoostingRegressor,
    air_density: xr.DataArray,
    absolute_wind_speed: xr.DataArray,
    wind_direction: xr.DataArray,
    time_of_day: xr.DataArray,
    time_of_year: xr.DataArray,
) -> xr.DataArray:
    """Predict the power production from given features.

    Features need to be identical to those used to train the model.

    """
    x = _prepare_x_values(
        air_density.values,
        absolute_wind_speed.values,
        wind_direction.values,
        time_of_day.values,
        time_of_year.values,
    )
    forecast = model.predict(x)
    production = xr.DataArray(
        forecast,
        coords=air_density.coords, 
        dims=air_density.dims, 
        name="production",
    )
    return production


def _prepare_x_values(*args) -> list:
    return list(zip(*args))
