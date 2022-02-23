import typing as t

import pandas as pd


def get_dates_as_strings(data: pd.DataFrame) -> t.List[str]:
    return list(data["date"].values)


def convert_to_columns(*columns):
    lengths = set(list(len(column) for column in columns))
    if len(lengths) != 1:
        raise ValueError("Input objects must have equal length")
    return [[*column] for column in zip(*columns)]
