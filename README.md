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
1. Currently, mantik supports developing bridges in Go, Scala, or Python.
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
