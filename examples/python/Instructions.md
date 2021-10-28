# Instructions for building a mantik bridge with Python

## Prerequisites
You will need
- Python 3.7 (required by [mantik](https://pypi.org/project/mantik/) and [mnp](https://pypi.org/project/mnp/))
- the Python dependency management tool `poetry`

## Creating a bridge
1. Start by copying an existing example and keep in mind you will need the following files:
   - a `.dockerignore` file to exclude large files to keep your Docker image small
   - located in the `src/` subdirectory:
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
   # Define the name of the bridge and its docker image.
   NAME = sklearn
   IMAGE_NAME = bridge.sklearn

   # Include all other necessary Makefiles.
   ROOT = ./../../../../
   include $(ROOT)/scripts/python/integrate.Makefile
   ```
   In the Makefile, define the
   - name of the bridge (`NAME=<bridge name>`)
   - name of the Docker image of the bridge (`IMAGE_NAME=bridge.<docker image name>`)
   **Note:** Avoid adapting any of the other variables.
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
4. In the `MantikHeader` (in `<bridge type>/<application>/MantikHeader`) define the bridge properties
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

   **Note:** mantik will put all the files located in the payload into your bridge
   when you execute it. As a result, any other utility functions or modules must
   be located in the payload to be used in the bridge.
7. Build the docker image of the bridge
   ```commandline
   make docker
   ```
8. Write a Python script to execute the bridge (see each bridge kind example below) and run it.

### `DataSet` bridges

1. For the `DataSetWrapper`, implement all methods of `mantik.bridge.DataSet`. Here, one option is
   to implement a `get` function in the payload. This can e.g. be achieved via
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

### `Algorithm` bridges

1. For the `AlgorithmWrapper`, implement all methods of `mantik.bridge.Algorithm` or `mantik.bridge.TrainableAlgorithm`,
   depending on whether you just want to implement data transformation or training of a model as well .
   Here, one option is to implement a `apply` and/or `train` function in the payload. This can e.g. be achieved via
   - `Algorithm`:
     ```Python

     import mantik


     # Wraps the supplied algorithm
     class AlgorithmWrapper(mantik.bridge.Algorithm):
         def __init__(self, mantikheader: mantik.types.MantikHeader):
             import sys

             sys.path.append(mantikheader.payload_dir)
             import algorithm

             self.apply_func = algorithm.apply
             self.mantikheader = mantikheader

         def apply(self, data: mantik.types.Bundle) -> mantik.types.Bundle:
             return self.apply_func(data, self.mantikheader.meta_variables)
     ```
   - `TrainableAlgorithm`:
      ```Python
      import os

      import mantik


      # Wraps the supplied algorithm
      class AlgorithmWrapper(mantik.bridge.TrainableAlgorithm):
           def __init__(self, mantikheader: mantik.types.MantikHeader):
              import sys

              sys.path.append(mantikheader.payload_dir)
              import algorithm

              self.train_func = algorithm.train
              self.try_init_func = algorithm.try_init
              self.apply_func = algorithm.apply
              self.is_trained_status = False
              self.model = None
              self.training_stats_result = None
              self.mantikheader = mantikheader

          @property
          def is_trained(self) -> bool:
              """Return whether the bridge has a trained model."""
              return self.is_trained_status

          @property
          def trained_data_dir(self) -> str:
              """Return the directory where the trained model is located."""
              return self.mantikheader.payload_dir

          def train(self, bundle) -> mantik.types.Bundle:
              """Train the bridge, i.e. a model."""
              old_pwd = os.getcwd()
              os.chdir(self.mantikheader.payload_dir)
              try:
                  stats = self.train_func(bundle, self.mantikheader.meta_variables)
                  # This should now work and not catch
                  self.model = self.try_init_func()
                  print("Reinitialized after successful learn")
                  self.training_stats_result = stats
                  self.is_trained_status = True
                  return stats
              finally:
                  os.chdir(old_pwd)

          @property
          def training_stats(self) -> mantik.types.Bundle:
              """Return the stats of the training step."""
              return self.training_stats_result

          def try_init_catching(self):
              """Initialize the bridge for applying the model.

              The model is loaded here to be available in the  apply  function.

              """
              old_pwd = os.getcwd()
              os.chdir(self.mantikheader.payload_dir)
              try:
                  self.model = self.try_init_func()
                  print("Successfully loaded Model...")
                  self.is_trained_status = True
              except Exception as e:
                  print(f"Could not load Model {e}")
              finally:
                  os.chdir(old_pwd)

          def apply(self, data) -> mantik.types.Bundle:
              """Apply the model, i.e. create a prediction."""
              if not self.is_trained_status:
                  raise Exception("Not trained")
              return self.apply_func(self.model, data)
      ```
2. Write the payload. For a dataset, it must include a `dataset.py`/`algorithm.py`
   file that has a `get`/`apply`/`train` method (or as you define it in the wrapper).

   **Note:** utility functions or modules must be located in the payload so that they can
   be used in the `dataset.get` method.

## Running the bridge
1. Start the mantik engine
   ```commandline
   docker-compose up
   ```
2. In the `datasets/<dataset name>/MantikHeader` or `algorithms/<algorithm name>/MantikHeader`,
   insert the correct bridge name for the  `bridge` field.
3. Write a script named `run.py` describing what bridges to execute or combine to a pipeline
   ```Python
   import pathlib

   import mantik

   __file_loc__ = pathlib.Path(__file__).parent

   with mantik.engine.Client("localhost", 8087) as client:
   # Submit all bridges to the engine
       dataset = client.add_artifact((__file_loc__ / "../../dataset/sklearn").as_posix())
       pandas = client.add_artifact((__file_loc__ / "../../algorithm/pandas").as_posix())
       sklearn = client.add_artifact(__file_loc__.as_posix())

       # Submit all payloads for each bridge to the engine.
       simple_dataset = client.add_artifact(
           (__file_loc__ / "../../dataset/sklearn/datasets/simple").as_posix()
       )
       transform = client.add_artifact(
           (__file_loc__ / "../../algorithm/pandas/algorithms/transform").as_posix()
       )
       transform2 = client.add_artifact(
           (__file_loc__ / "../../algorithm/pandas/algorithms/transform2").as_posix()
       )
       kmeans = client.add_artifact((__file_loc__ / "algorithms/simple").as_posix())

       # Start a mantik session.
       with client.enter_session():
           # Train the model on the given dataset.
           # Before training the kmeans model, the two tansform actions will
           # be performed on the dataset.
           trained_pipe, stats = client.train(
               pipeline=[transform, transform2, kmeans],
               data=simple_dataset,
           )
           print(f"Stats: {stats.bundle.value}")

           # Apply the kmeas model on a given dataset.
           result = client.apply(trained_pipe, simple_dataset)
           print(f"Apply result: {result.bundle.value}")
   ```
5. Run the `run.py` script
   ```commandline
   poetry run python run.py
   ```
   or
   ```commandline
   make run
   ```
