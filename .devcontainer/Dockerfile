# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.231.6/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN export DEBIAN_FRONTEND=noninteractive

# Install AWS CDK toolkit
RUN apt-get update && apt-get -y install --no-install-recommends awscli git
RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g aws-cdk" 2>&1

# Installing the AWS Session Manager so we can use SSM to SSH/Exec onto instances/containers
RUN  cpuversion=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/64bit/) && \
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_${cpuversion}/session-manager-plugin.deb" -o "/tmp/session-manager-plugin.deb"
RUN dpkg -i /tmp/session-manager-plugin.deb

RUN cp requirements.txt . && \
    pip install -r requirements.txt