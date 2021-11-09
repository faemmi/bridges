# Set local mantik core repo path
MANTIK_ROOT ?= /home/fabian/work/mantik/core
build: install clean
	mkdir -p target
	# Copy bridge files to target
	$(call COPY_PYTHON_FILES,src/,target/)
	cp poetry.lock pyproject.toml target/

	# Copy local python sdk and mnppython files
	$(call COPY_PYTHON_FILES,$(MANTIK_ROOT)/python_sdk,target/)
	$(call COPY_PYTHON_FILES,$(MANTIK_ROOT)/mnp/mnppython,target/)

	# Rewrite relative paths to allow installation of the packages
	sed -i 's/".*python_sdk"/"\.\/python_sdk"/' target/poetry.lock target/pyproject.toml
	sed -i 's/".*mnppython"/"\.\/mnppython"/' target/poetry.lock target/pyproject.toml
	sed -i 's/".*mnppython"/"\.\/..\/mnppython"/' target/python_sdk/poetry.lock target/python_sdk/pyproject.toml

.PHONY: build
