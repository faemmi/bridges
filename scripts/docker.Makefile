# Shared code for building a single Docker Image

# Needed Variables
# IMAGE_NAME: name of the final Docker image
# MANTIK_VERSION: version of mantik this bridge is compatible with
# There are also some optional arguments below
DOCKER ?= docker
DOCKER_IMAGE_NAME = $(IMAGE_NAME):$(MANTIK_VERSION)
DOCKER_REPO ?= mantikai
DOCKER_IMAGE_FULL_NAME = $(DOCKER_REPO)/$(DOCKER_IMAGE_NAME)


# Credentials for publishing the image
DOCKER_USERNAME ?= $(DOCKER_USERNAME)
DOCKER_PASSWORD ?= $(DOCKER_PASSWORD)

DOCKER_EXTRA_ARGS ?=

# If given, use this docker file
DOCKER_FILE ?= ""

ifeq ($(DOCKER_FILE),"")
	DOCKER_FILE_ARGUMENT =
else
	DOCKER_FILE_ARGUMENT = -f $(DOCKER_FILE)
endif

docker: clean build docker-unchecked

docker-unchecked:
	# Build Docker image $(DOCKER_IMAGE_FULL_NAME)
	$(DOCKER) build $(DOCKER_FILE_ARGUMENT) $(DOCKER_EXTRA_ARGS) -t $(DOCKER_IMAGE_FULL_NAME) .

docker-login:
	@# Trick to not show the password
	@mkdir -p target
	@touch target/docker_password
	@chmod 600 target/docker_password
	@echo $(DOCKER_PASSWORD) > target/docker_password
	cat target/docker_password | $(DOCKER) login -u $(DOCKER_USERNAME) --password-stdin $(DOCKER_REPO)
	@rm -r target/

docker-publish: docker-login
	# Publish Docker image
	$(DOCKER) push $(DOCKER_IMAGE_FULL_NAME)

.PHONY: docker docker-unchecked docker-login docker-publish
