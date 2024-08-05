PYTHON ?= python3
SOURCES := src
TOOLS := tools
ROOT_DIR ?= $(shell git rev-parse --show-toplevel)

# Version
RELEASE_VERSION ?= $(shell git rev-parse --short HEAD)_$(shell date -u +%Y-%m-%dT%H:%M:%S%z)
GIT_BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD)
GIT_COMMIT ?= $(shell git rev-parse --verify HEAD)

.PHONY: help build clean

help:
	@echo "TodoList development makefile"
	@echo
	@echo "Usage: make <TARGET>"
	@echo
	@echo "Target:"
	@echo "  build               Build docker image."
	@echo "  clean               Clean all invalid files and folders."
	@echo

BUILD_CONTEXT ?= .
DOCKER_FILE ?= Dockerfile
IMAGE ?= todolist
IMAGE_TAG ?= latest
build:
	docker build --no-cache --pull --force-rm --build-arg RELEASE_VERSION=$(RELEASE_VERSION) --build-arg GIT_BRANCH=$(GIT_BRANCH) --build-arg GIT_COMMIT=$(GIT_COMMIT) $(BUILD_ARGS) -f $(DOCKER_FILE) -t $(IMAGE):$(IMAGE_TAG) $(BUILD_CONTEXT)

clean:
	rm -rf .mypy_cache
	rm -rf mypy-report
	rm -rf todolist.egg-info
	find . -name '__pycache__' | xargs rm -rf
	rm -rf AUTHORS
	rm -rf ChangeLog
