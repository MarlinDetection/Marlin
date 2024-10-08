# Build from Ubuntu 22 image
FROM ubuntu:jammy

# Standard environment variables
# ENV DEBIAN_FRONTEND=noninteractive
# ENV TZ=America/New_York

# Download dependencies
RUN apt-get update
RUN apt-get install -y python3.10-venv python3-pip git python3-dev tshark

# Download Marlin code
WORKDIR /
RUN git clone https://github.com/MarlinDetection/Marlin

# Create and start virtual environment
WORKDIR /Marlin/code
RUN python3 -m venv ./venv
RUN source ./venv/bin/activate
RUN	python3 -m pip install -r requirements.txt
WORKDIR /Marlin/analysis