FROM ubuntu:latest

# this will be the base dir of our app
WORKDIR /app

# copy requirements to temporary file
COPY ./requirements.txt /tmp/requirements.txt

# install packages
# /var/lib/apt/lists contains apt lists and would only bloat docker image
## python
RUN apt update &&  apt install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
## python packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# now copy source code
# doing dependencies and sourcecode separately improves caching
COPY ./ ./

# install backend package
RUN pip install -e .

# run backend
CMD ["python3", "run.py"]
