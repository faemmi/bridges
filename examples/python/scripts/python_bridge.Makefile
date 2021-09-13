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

target/copy_py.make: $(shell find . -name "*.py" -not -path "./target/*" -not -path "./example/*")
	mkdir -p target
	rsync -R $? target/
	touch $@

target/copy_shared.make: $(shell find $(MANTIK_ROOT)/python_sdk -name "*.py")
	mkdir -p target
	cp poetry.lock pyproject.toml target/

	# Below is just for local developing
	cp -v -r $(ROOT_DIR)/core/python_sdk target/
	cp -v -r $(ROOT_DIR)/core/mnp/mnppython target/

	# Rewrite relative paths to allow installation of the packages
	sed -i 's/".*python_sdk"/"\.\/python_sdk"/' target/poetry.lock target/pyproject.toml
	sed -i 's/".*mnppython"/"\.\/mnppython"/' target/poetry.lock target/pyproject.toml
	sed -i 's/".*mnppython"/"\.\/..\/mnppython"/' target/python_sdk/poetry.lock target/python_sdk/pyproject.toml

	touch $@

.PHONY: api-doc build clean test publish
