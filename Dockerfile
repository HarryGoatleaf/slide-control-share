FROM ubuntu:latest

# this will be the base dir of our app
WORKDIR /app

# copy source to workdir
COPY ./slide-control-share ./

# install packages
# /var/lib/apt/lists contains apt lists and would only bloat docker image
## python
RUN apt update && apt install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
## python packages
RUN pip install --no-cache-dir -r ./requirements.txt