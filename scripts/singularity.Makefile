# Shared code for building a single Docker Image

# Needed Variables
# IMAGE_NAME: name of the final Docker image
# MANTIK_VERSION: version of mantik this bridge is compatible with
# There are also some optional arguments below
SINGULARITY ?= singularity
SINGULARITY_IMAGE_NAME = $(IMAGE_NAME):$(MANTIK_VERSION)

# Below variable DOCKER_REPO is defined in docker.Makefile
SINGULARITY_IMAGE_PREFIX ?= $(DOCKER_REPO)-
SINGULARITY_IMAGE_FULL_NAME = $(SINGULARITY_IMAGE_PREFIX)$(SINGULARITY_IMAGE_NAME).sif


# Credentials for publishing the image
SINGULARITY_REGISTRY ?= SyslabsCloud
SINGULARITY_USERNAME ?= $(SINGULARITY_USERNAME)
SINGULARITY_REPO ?= default
SINGULARITY_TOKEN ?= $(SINGULARITY_TOKEN)
SINGULARITY_LIBRARY ?= library
SINGULARITY_PUSH_TARGET = $(SINGULARITY_LIBRARY)://$(SINGULARITY_USERNAME)/${SINGULARITY_REPO:+$SINGULARITY_REPO/}/$(SINGULARITY_IMAGE_FULL_NAME)

SINGULARITY_EXTRA_ARGS ?=

# Use this source for fetching the Docker image
DOCKER_SOURCE ?= docker-daemon

# Below variable DOCKER_IMAGE_FULL_NAME is defined in docker.Makefile
define SINGULARITY_BUILD_RECIPE
bootstrap: $(DOCKER_SOURCE)
from: $(DOCKER_IMAGE_FULL_NAME)

%startscript
    cd /opt/bridge
    . /venv/bin/activate
    python main.py
endef

export SINGULARITY_BUILD_RECIPE

singularity: clean build docker singularity-build

singularity-build:
	# Create Singularity build recipe
	@mkdir -p target
	@touch target/recipe.def
	@echo "$${SINGULARITY_BUILD_RECIPE}" > target/recipe.def

	# Build Singularity image $(SINGULARITY_IMAGE_FULL_NAME)
	# NOTE: Building is going to need sudo!
	sudo $(SINGULARITY) build --force $(SINGULARITY_EXTRA_ARGS) $(SINGULARITY_IMAGE_FULL_NAME) target/recipe.def

	@rm target/recipe.def

singularity-sign:
	# Sign image $(SINGULARITY_IMAGE_FULL_NAME)
	singularity sign $(SINGULARITY_IMAGE_FULL_NAME)

singularity-login:
	@# Trick to not show the password
	@mkdir -p target
	@touch target/singularity_token
	@chmod 600 target/singularity_token
	@echo $(SINGULARITY_TOKEN) > target/singularity_token

	# Log into $(SINGULARITY_REGISTRY)
	cat target/singularity_token | $(SINGULARITY) remote login --password-stdin $(SINGULARITY_REGISTRY)

	@rm target/singularity_token

singularity-publish: singularity-sign singularity-login
	# Publish singularity image to $(SINGULARITY_PUSH_TARGET)
	$(SINGULARITY) push $(SINGULARITY_IMAGE_FULL_NAME) $(SINGULARITY_PUSH_TARGET)

.PHONY: singularity singularity-sign singularity-build singularity-login singularity-publish
