# Build from Ubuntu 20 image
FROM ubuntu:focal

# Standard environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Download dependencies
RUN apt update
RUN apt install -y python3-venv python3-pip git python3-dev tshark

# Download Marlin code
WORKDIR /
RUN git clone https://github.com/MarlinDetection/Marlin

# Create and start virtual environment
WORKDIR /Marlin/code
RUN python3 -m venv ./venv
RUN /bin/bash -c 'source ./venv/bin/activate'
RUN	python3 -m pip install -r requirements.txt
WORKDIR /Marlin/code/analysis
