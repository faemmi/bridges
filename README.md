# bridges
Tutorials for building [mantik](https://github.com/mantik-ai/core) bridges.

## Prerequisites
The mantik engine will be deployed locally in Docker using a Docker Compose file.
Furthermore, Makefiles will be used in each example to build the bridges (i.e. as Docker containers).
Hence, you need
- Docker
- Docker Compose
- make

## Building a bridge

1. Start up the mantik engine in Docker locally
   ```commandline
   docker-compose -f scripts/docker-compose.engine.yaml up
   ```
2. Currently, mantik supports developing bridges in Go, Scala, or Python.
   Follow the instructions for the respective language in `examples/<language>/Instructions.md`.

## Maintaining good code quality

### Python
To achieve working and readable code, use `pre-commit`:
1. Install the framework
   ```commandline
   pip install pre-commit
   ```
2. Install the hooks
   ```commandline
   pre-commit install
   ```
3. The pre-commit hooks now get automatically executed at each commit.
   Alternatively, you can run them on all files:
   ```commandline
   pre-commit run --all
   ```

## Using a local version of mantik and mnp for developing Python bridges

To use a local version of mantik and mnp, the `Makefile` of a bridge as well as the `pyproject.toml` and
the `scripts/bridge-dev.Makefile` have to be adapted.

- `scripts/bridge-dev.Makefile`: set the `MANTIK_ROOT` variable to the local path of the mantik core repository,
  where the mantik Python SDK and mnp for Python are located.
- `pyproject.toml`: replace the mantik dependency with a local dependency and add mnp as a local dependency as
  ```toml
  mantik = { path = "<local path to mantik core repo>/python_sdk", develop = true }
  ```
  **Note:** mantik depends on mnp, hence the local version of mnp is installed as well.
- `Makefile`: instead of the `scripts/integrate.Makefile`, use `scripts/integrate-dev.Makefile`, i.e. replace
  ```make
  include $(ROOT)/scripts/python/integrate.Makefile
  ```
  with
  ```make
  include $(ROOT)/scripts/python/integrate-dev.Makefile
  ```
