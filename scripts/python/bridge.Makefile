MAKEFLAGS += --no-builtin-rules

# Set the Docker image tag and create the final Docker image name
MANTIK_VERSION = $(shell poetry version -s)

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

run: install
	poetry run python run.py

test: install
	poetry run pytest

integration-test: run

clean:
	rm -rf target

.PHONY: build run test integration-test clean
