# Define the name of the bridge and its docker image
NAME = dataset.production
MANTIK_VERSION=v0.3.0-rc6
IMAGE_NAME=bridge.dataset.production
DOCKER_IMAGE_NAME=$(IMAGE_NAME):$(MANTIK_VERSION)

# Include all other necessary Makefiles.
PYTHON_SCRIPTS=./../../../../scripts
include  $(PYTHON_SCRIPTS)/Makefile.integrate
