MAKEFLAGS += --no-builtin-rules

# Set the Docker image tag and create the final Docker image name
MANTIK_VERSION = $(shell poetry version -s)

build:
	mkdir -p target
	rsync -a --prune-empty-dirs \
	    --include '*.py' \
	    --exclude=__pycache__/ \
	    --exclude=.pytest_cache/ \
	    src/ target/
	cp poetry.lock pyproject.toml target/

clean:
	rm -rf target

test:
	poetry install
	poetry run pytest

integration-test:
	poetry install
	poetry run python execute.py

.PHONY: build clean test integration-test
