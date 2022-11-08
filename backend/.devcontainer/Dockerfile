FROM mcr.microsoft.com/vscode/devcontainers/python:3

# this will be the base dir of our app
WORKDIR /app

# copy source to workdir
# COPY ./slide-control-share ./

# copy requirements to temporary file
COPY ./requirements.txt /tmp/requirements.txt

## python packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt
