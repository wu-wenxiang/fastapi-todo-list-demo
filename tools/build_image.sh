#!/bin/bash

DOCKER_NAME=todolist
DOCKER_IMAGE=registry.cn-shanghai.aliyuncs.com/99cloud-sh/skyline/${DOCKER_NAME}

RELEASE_VERSION=`git rev-parse --short HEAD`_`date -u +%Y-%m-%dT%H:%M:%S%z`
GIT_BRANCH=`git rev-parse --abbrev-ref HEAD`
GIT_COMMIT=`git rev-parse --verify HEAD`
docker build --no-cache --pull --force-rm --build-arg RELEASE_VERSION=${RELEASE_VERSION} --build-arg GIT_BRANCH=${GIT_BRANCH} --build-arg GIT_COMMIT=${GIT_COMMIT} -f Dockerfile -t ${DOCKER_IMAGE} .

# push to docker registry
docker push ${DOCKER_IMAGE}
