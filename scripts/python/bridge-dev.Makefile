MAKEFLAGS += --no-builtin-rules

# Set the Docker image tag and create the final Docker image name
MANTIK_VERSION = $(shell poetry version -s)

# Set local mantik core repo path
MANTIK_ROOT ?=

install:
	poetry install

build: install clean
	mkdir -p target
	rsync -a --prune-empty-dirs \
	    --include '*.py' \
	    --exclude=__pycache__/ \
	    --exclude=.pytest_cache/ \
	    src/ target/
	cp poetry.lock pyproject.toml target/

	# Copy local python sdk and mnppython files
	cp -v -r $(MANTIK_ROOT)/python_sdk target/
	cp -v -r $(MANTIK_ROOT)/mnp/mnppython target/

	# Rewrite relative paths to allow installation of the packages
	sed -i 's/".*python_sdk"/"\.\/python_sdk"/' target/poetry.lock target/pyproject.toml
	sed -i 's/".*mnppython"/"\.\/mnppython"/' target/poetry.lock target/pyproject.toml
	sed -i 's/".*mnppython"/"\.\/..\/mnppython"/' target/python_sdk/poetry.lock target/python_sdk/pyproject.toml

run: install
	poetry run python run.py

test: install
	poetry run pytest

integration-test: run

clean:
	rm -rf target

.PHONY: build run test integration-test clean
