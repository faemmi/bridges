import pickle
import typing as t

MODEL_FILE = "model.pickle"


def prepare_x_values(*args) -> t.List:
    return list(zip(*args))


def save_model(model):
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)


def load_model():
    with (open(MODEL_FILE, "rb")) as f:
        return pickle.load(f)
