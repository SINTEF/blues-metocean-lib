from python:3.8-slim

RUN python -m pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y  libnetcdf-dev gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

