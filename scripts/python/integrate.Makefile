# Include all other necessary make files
SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
ROOT = ${SELF_DIR}/../../
DOCKER_FILE = $(ROOT)/scripts/python/bridge.Dockerfile
include $(ROOT)/scripts/python/bridge.Makefile
include $(ROOT)/scripts/docker.Makefile
include $(ROOT)/scripts/singularity.Makefile
