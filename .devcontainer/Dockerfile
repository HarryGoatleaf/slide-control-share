FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# copy source to workdir
# COPY ./src ./

# install packages
# /var/lib/apt/lists contains apt lists and would only bloat docker image
## python
RUN apt update && apt install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
## install python packages in devcontainer.json because there src is mounted
