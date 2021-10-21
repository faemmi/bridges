# Define the name of the bridge and its docker image
NAME=pandas
MANTIK_VERSION=$(shell poetry version -s)
IMAGE_NAME=bridge.pandas
DOCKER_IMAGE_NAME=$(IMAGE_NAME):$(MANTIK_VERSION)

# Include all other necessary Makefiles.
PYTHON_SCRIPTS=./../../../scripts
include $(PYTHON_SCRIPTS)/integrate.Makefile
