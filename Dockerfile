FROM ubuntu:22.04

ARG GIT_BRANCH
ARG GIT_COMMIT
ARG RELEASE_VERSION

LABEL todolist.build_branch=${GIT_BRANCH}
LABEL todolist.build_commit=${GIT_COMMIT}
LABEL todolist.release_version=${RELEASE_VERSION}

COPY ./ /todolist/

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN export LANG=C.UTF-8 \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends apt-utils \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y iputils-ping vim git python3-pip python3 tzdata supervisor \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && rm -rf /etc/timezone \
    && cd /todolist/ \
    && git init \
    && git config --global user.name build \
    && git config --global user.email build@mail.com \
    && git add . \
    && git commit -a -m "Build ${GIT_BRANCH} ${GIT_COMMIT}" \
    && cd / \
    && pip install --index-url https://mirrors.aliyun.com/pypi/simple/ todolist/ \
    && apt-get clean \
    && rm -rf ~/.cache/pip

COPY ./etc/todolist/gunicorn.py.sample /etc/todolist/gunicorn.py
COPY ./etc/todolist/todolist.conf.sample /etc/todolist/todolist.conf
COPY ./etc/todolist/logging.conf.sample /etc/todolist/logging.conf
COPY ./etc/todolist/supervisord.conf.sample /etc/todolist/supervisord.conf
COPY ./etc/todolist/celeryconfig.py.sample /todolist/todolist/tasks/celeryconfig.py
COPY ./tools/run_service.sh /usr/local/bin/run_service.sh
