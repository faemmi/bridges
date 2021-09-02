import xarray as xr


def calculate_pressure(
    p_s: xr.DataArray,
    constants: xr.Dataset,
    model_level: int,
) -> xr.DataArray:
    """Calculate the pressure at a certain model level.

    Parameters
    ----------
    p_s : pd.Series
        Pressure at surface level.
    constants : pd.DataFrame
        Constants hayi, hybi, hyam, hybm as from the `maelstrom-constants-a-b` dataset.

    Returns
    -------
    pandas.Series
        Pressure for a given model level.

    """
    _, _, A_1, B_1 = constants.loc[(0, model_level - 1)]
    _, _, A_2, B_2 = constants.loc[(0, model_level)]
    p_1 = _calculate_pressure_levels(p_s, A_k=A_1, B_k=B_1)
    p_2 = _calculate_pressure_levels(p_s, A_k=A_2, B_k=B_2)
    p = 0.5 * (p_1 + p_2)
    return p


def _calculate_pressure_levels(
    p_s: float, A_k: xr.DataArray, B_k: xr.DataArray
) -> xr.DataArray:
    """Calculate the pressure for each model level.

    Parameters
    ----------
    p_s : float
        Pressure at surface level.
    A_k : pd.Series
        Constant for each model level.
    B_k : pd.Series
        Constant for each model level.

    Returns
    -------
    pandas.Series
        Pressure for each model level.

    """
    return A_k + B_k * p_s
