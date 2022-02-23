import mantik


def unpack_bundle(bundle: mantik.types.Bundle) -> tuple:
    columns = len(bundle.value[0])
    return tuple(tuple(row[i] for row in bundle.value) for i in range(columns))


def convert_to_columns(*columns):
    lengths = set(list(len(column) for column in columns))
    if len(lengths) != 1:
        raise ValueError("Input objects must have equal length")
    return [[*column] for column in zip(*columns)]
