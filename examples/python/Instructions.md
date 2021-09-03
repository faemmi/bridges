# Instructions for building a mantik bridge with Python

## Prerequisites
You will need
- Python 3.7 (required by [mantik](https://pypi.org/project/mantik/) and [mnp](https://pypi.org/project/mnp/))
- the Python dependency management tool `poetry`

## Creating the bridge
1. Write the bridge.

**Note:** As long as a DataSet bridge does not exist, the production
example has to include the `data` dir (its included by the `Dockerfile.python_bridge`).
The simple example, however, does **not** need to include the data directory. Hence, when
building the simple bridge, the two lines including the data directory have to be
commented out.

## Running the bridge
1. Run the `train_algorithm.py` script
   ```commandline
   poetry run python train_algorithm.py
   ```
