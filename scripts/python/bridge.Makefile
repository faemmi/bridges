MAKEFLAGS += --no-builtin-rules

# Set the Docker image tag and create the final Docker image name
MANTIK_VERSION = $(shell poetry version -s)

define COPY_PYTHON_FILES
	rsync -a --prune-empty-dirs \
	    --include '*.py' \
	    --exclude '*.pyc' \
	    --exclude '*.pyo' \
	    --exclude=__pycache__/ \
	    --exclude=tests/ \
	    --exclude=.pytest_cache/ \
	    --exclude=target/ \
	    --exclude '\.*' \
	    --exclude 'Makefile' \
	    $(1) $(2)
endef

define DELETE_PYTHON_CACHE_FILES
    # Delete Python cache files
    find . | grep -E "(__pycache__|.pytest_cache|\.pyc|\.pyo$$)" | xargs rm -rf
endef

install:
	poetry lock --no-update
	poetry install

build: install clean
	mkdir -p target
	# Copy bridge files to target
	cp poetry.lock pyproject.toml target/
	$(call COPY_PYTHON_FILES,src/,target/)

run: install
	poetry run python run.py

test: install
	poetry run pytest

integration-test: run

clean:
	rm -rf target
	$(call DELETE_PYTHON_CACHE_FILES)

.PHONY: build run test integration-test clean
