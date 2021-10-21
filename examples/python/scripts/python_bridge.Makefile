MAKEFLAGS += --no-builtin-rules
# Note: the root dir path here is relative to the directory where the
# base Makefile is being executed. This is supposed to be
# `examples/python/bridges/<kind>/<framework>/Makefile`.
ROOT_DIR = ./../../../../../../

# Caching
ifdef CACHE_DIR
  export POETRY_CACHE_DIR_PATH=$(CACHE_DIR)/poetry
endif


build: target/build.make

clean::
	rm -rf target

test:
	POETRY_CHACHE_DIR=$(POETRY_CACHE_DIR_PATH) poetry install
	POETRY_CHACHE_DIR=$(POETRY_CACHE_DIR_PATH) poetry run pytest

target/build.make: target/copy_py.make target/copy_shared.make
	touch $@

target/copy_py.make: $(shell find . -name "*.py" -not -path "./target/*" -not -path "./algorithms/*" -not -path "./datasets/*")
	mkdir -p target
	rsync -R $? target/
	touch $@

target/copy_shared.make:
	mkdir -p target
	cp poetry.lock pyproject.toml target/

	touch $@

.PHONY: api-doc build clean test publish
