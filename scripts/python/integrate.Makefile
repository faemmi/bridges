# Include all other necessary make files
SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
ROOT = ${SELF_DIR}/../../
DOCKER_FILE = $(SELF_DIR)/bridge.Dockerfile
include $(SELF_DIR)/bridge.Makefile
include $(ROOT)/scripts/docker.Makefile
include $(ROOT)/scripts/singularity.Makefile
