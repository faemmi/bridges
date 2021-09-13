# Include all other necessary make files
# Note: the paths here are relative to the directory where the 
# base Makefile is being executed. This is supposed to be 
# `examples/python/bridges/<kind>/<framework>/Makefile`.
ROOT=./../../../../../
PYTHON_ROOT=./../../../
DOCKER_FILE=$(PYTHON_ROOT)/scripts/python_bridge.Dockerfile
include $(PYTHON_ROOT)/scripts/python_bridge.Makefile
include $(ROOT)/scripts/docker_single.Makefile
