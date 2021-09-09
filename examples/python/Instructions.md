# Instructions for building a mantik bridge with Python

## Prerequisites
You will need
- Python 3.7 (required by [mantik](https://pypi.org/project/mantik/) and [mnp](https://pypi.org/project/mnp/))
- the Python dependency management tool `poetry`

## Creating the bridge
1. Write the bridge.
2. In the `Makefile`, define the 
   - name of the bridge (`NAME=<bridge name>`)
   - name of the Docker image of the bridge (`DOCKER_IMAGE_NAME=bridge.<docker image name>`)
   **Note:** Avoid adapting any of the other variables
3. In the `pyproject.toml`, define all package information dependencies and 3rd-party dependencies
   ```toml
   [tool.poetry]
   name = "mantik-<bridge name>-bridge"
   description = "Mantik bridge for <application>"
   version = "<version of mantik>"
   authors = ["<Your name> <<your email>>"] # Note that the email is inside `<>`
   homepage = "https://www.mantik.ai"
   
   [tool.poetry.dependencies]
   python = "~3.7"  # required by mantik
   mantik = "0.3.0-rc6"  # version of mantik that is used in the bridge, will also include `mnp`
   <any other 3rd-party dependencies go here>
   
   [tool.poetry.dev-dependencies]
   pytest = "^6.2.4"  # for testing the bridge implementation
   
   [build-system]
   requires = ["poetry>=1.0.0"]
   
   [tool.pytest.ini_options]
   norecursedirs = "target"
   ```
   **Note:** Each time when you update a dependency, you need to run `poetry lock` to
   update the `poetry.lock` file, which is used by poetry to install the dependencies.
4. In the `MantikHeader` (in `bridges/<bridge type>/<application>/MantikHeader`) define the bridge properties
   that are relevant for the mantik engine
   ```YAML
   kind: bridge
   account: mantik
   name: <application>
   suitable:
     - <list of suitables>
   dockerImage: mantikai/bridge.<application>
   protocol: 1
   ```
   Possible suitables (i.e. bridge kinds) are:
     - dataset
     - algorithm
     - trainable
5. Write the `main.py`, `<kind>_wrapper.py`, and payloads.
6. Build the docker image of the bridge
   ```commandline
   make docker
   ```

**Note:** As long as a DataSet bridge does not exist, the production
example has to include the `data` dir (its included by the `Dockerfile.python_bridge`).
The simple example, however, does **not** need to include the data directory. Hence, when
building the simple bridge, the two lines including the data directory have to be
commented out.

## Running the bridge
1. In the `algorithms/<algorithm name>/MantikHeader`, insert the correct bridge name for 
   the  `bridge` field.
2. Run the `train_algorithm.py` script
   ```commandline
   poetry run python train_algorithm.py
   ```
