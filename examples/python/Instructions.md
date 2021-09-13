# Instructions for building a mantik bridge with Python

## Prerequisites
You will need
- Python 3.7 (required by [mantik](https://pypi.org/project/mantik/) and [mnp](https://pypi.org/project/mnp/))
- the Python dependency management tool `poetry`

## Creating a bridge
1. Start by copying an existing example and keep in mind you will need the following files:
   - a `.dockerignore` file to exclude large files to keep your Docker image small
   - a wrapper file for your bridge kind from `mantik.bridge.kinds` (e.g. `algorithm_wrapper.py`)
   - a `main.py` file that tells the mantik engine how to start your bridge that looks like
     ```Python
     import mantik

     from algorithm_wrapper import AlgorithmWrapper


     def create_algorithm(mantikheader: mantik.types.MantikHeader):
         algorithm = AlgorithmWrapper(mantikheader)
         return algorithm


     mantik.bridge.start_mnp_bridge(create_algorithm, "Pandas Bridge")

     ```
   - a `Makefile` for building the Docker image (see below)
   - a `MantikHeader` file to define your bridge so that mantik can understand it
     (for details see below)
   - a `pyproject.toml` file for managing your bridge's
     dependencies (i.e. third-party packages it implements)
2. A blueprint of a Makefile looks as follows
   ```bash
   # Define the name of the bridge and its docker image
   NAME=<bridge name>
   MANTIK_VERSION=<mantik version the bridge was designed for>
   IMAGE_NAME=bridge.<bridge name>
   # AVOID CHANGES BELOW HERE
   DOCKER_IMAGE_NAME=$(IMAGE_NAME):$(MANTIK_VERSION)

   # Include all other necessary Makefiles.
   PYTHON_SCRIPTS=./../../../scripts
   include $(PYTHON_SCRIPTS)/integrate.Makefile
   ```
   In the Makefile, define the
   - name of the bridge (`NAME=<bridge name>`)
   - name of the Docker image of the bridge (`DOCKER_IMAGE_NAME=bridge.<docker image name>`)
   **Note:** Avoid adapting any of the other variables
3. In the `pyproject.toml`, define all package information dependencies and 3rd-party dependencies
   ```toml
   [tool.poetry]
   name = "mantik-<bridge name>-bridge"
   description = "Mantik bridge for <application>"
   version = "<version of mantik the bridge is designed for>"
   authors = ["<Your name> <<your email>>"] # Note that the email is inside `<>`
   homepage = "https://www.mantik.ai"

   [tool.poetry.dependencies]
   python = "~3.7"  # required by mantik
   mantik = "<mantik version>"  # version of mantik that is used in the bridge
   <any other 3rd-party dependencies go here>

   [tool.poetry.dev-dependencies]
   pytest = "^6.2.4"  # for testing the bridge implementation

   [build-system]
   requires = ["poetry>=1.0.0"]

   [tool.pytest.ini_options]
   norecursedirs = "target"  # to avoid testing file copies
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
5. Write the `main.py`, `<kind>_wrapper.py`, and payloads (for details, see below).
   Note: mantik will put all the files located in the payload into your bridge
   when you execute it. As a result, any other utility functions or modules must
   be located in the payload to be used in the bridge.
6. Build the docker image of the bridge
   ```commandline
   make docker
   ```
7. Write a Python script to execute the bridge (see each bridge kind example below) and run it.

**Note:** As long as a DataSet bridge does not exist, the production
example has to include the `data` dir (it's included by the `Dockerfile.python_bridge`).
The simple example, however, does **not** need to include the data directory. Hence, when
building the simple bridge, the two lines including the data directory have to be
commented out.

### DataSet bridges

1. For the `DataSetWrapper`, implement all methods of `mantik.bridge.DataSet`. Here, the wrapper additionally
   has to implement the get function of the payload. This can e.g. be achieved via
   ```Python
   import mantik


   # Wraps the supplied DataSet
   class DataSetWrapper(mantik.bridge.DataSet):
       def __init__(self, mantikheader: mantik.types.MantikHeader):
           # Within your payload, write a `dataset.py` file
           # that implements a method named `get`, and import it here.
           # Note: This *must* be done within a function of the wrapper
           # or the import will fail.
           import sys
           sys.path.append(mantikheader.payload_dir)
           import dataset

           self.get_func = dataset.get
           self.mantikheader = mantikheader

       def get(self) -> mantik.types.Bundle:
           return self.get_func(self.mantikheader.meta_variables)

   ```
2. Write the payload. For a dataset, it must include a `dataset.py`
   file that has a `get` method (or as you define it in the wrapper).
   The function has to follow the given pattern:
   ```Python
   def get(meta: mantik.types.MetaVariables) -> mantik.types.Bundle:
      ...
   ```
   Reminder: utility functions or modules must be located in the payload so that they can
   be used in the `dataset.get` method.

## Running the bridge
1. Start the mantik engine
   ```commandline
   docker-compose up
   ```
2. In the `algorithms/<algorithm name>/MantikHeader`, insert the correct bridge name for
   the  `bridge` field.
3. Run the `get_dataset.py`/`apply_algorithm.py`/`train_algorithm.py` script
   ```commandline
   poetry run python <script name>.py
   ```
