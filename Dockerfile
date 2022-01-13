# syntax=docker/dockerfile:1
FROM debian:stable

# Package installs/updates:
RUN apt-get update -y && apt-get install -y wget curl unzip libgconf-2-4
RUN apt-get update -y && apt-get install -y chromium python3 python3-pip

# Install latest chromedriver
RUN wget https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
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