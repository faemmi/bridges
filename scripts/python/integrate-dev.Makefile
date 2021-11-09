# Include all other necessary make files
SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(SELF_DIR)/integrate.Makefile
include $(SELF_DIR)/bridge-dev.Makefile
