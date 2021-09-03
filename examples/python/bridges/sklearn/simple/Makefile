# Define the name of the bridge and its docker image
NAME = sklearn.simple
DOCKER_IMAGE_NAME=bridge.sklearn.simple

# Include all other necessary make files
ROOT=./../../../../../
PYTHON_ROOT=$(ROOT)/examples/python
DOCKER_FILE=$(PYTHON_ROOT)/scripts/Dockerfile.python_bridge
include $(PYTHON_ROOT)/scripts/Makefile.python_bridge
include $(ROOT)/scripts/Makefile.docker_single

