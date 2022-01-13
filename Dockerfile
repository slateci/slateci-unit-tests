# syntax=docker/dockerfile:1
FROM python:3.9.9-buster

# Docker container environmental variables:
ENV CHROMEDRIVER_VERSION=96.0.4664.45

# Package installs/updates:
RUN apt-get update -y && apt-get install -y wget curl unzip libgconf-2-4
RUN apt-get update -y && apt-get install -y chromium xvfb python3 python3-pip

# Install chromedriver
RUN wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
RUN unzip ./chromedriver_linux64.zip chromedriver -d /usr/local/bin/ && \
    rm ./chromedriver_linux64.zip

# Install Python dependencies:
COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt && \
    rm ./requirements.txt

# Set the project directory:
RUN mkdir /opt/project

# Set the work directory:
WORKDIR /opt/project

# Volumes
VOLUME [ "/opt/project" ]