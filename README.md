# Detecting IMSI-Catchers by Characterizing Identity Exposing Messages in Cellular Traffic

We provide our code using Docker containers and a Python virtual environment to minimize platform dependency issues. To run our containers, you must have [Python3](https://www.python.org/downloads/) and [Docker](https://docs.docker.com/engine/install/) installed on your machine.

Additionally, you need at least one software-defined radio (SDR) supported by srsRAN to run LTE analysis and at least one SDR support by gr-gsm to run GSM analysis. We confirmed that our LTE code works with the [Ettus Research USRP B210](https://www.ettus.com/all-products/ub210-kit/).

## Docker

All Dockerfiles are located under the `./docker` directory, which includes subdirectories for each cellular program. You must build each image using `sudo docker build -t .` from within those subdirectories. Since we are using USB devices, we must pass through the `/dev` directory when creating each container. We share further run instructions in a README within `./docker`.

## Analysis

Our program writes packet captures in `.pcap` format, which can be viewed directly in [Wireshark](https://www.wireshark.org/). For detailed traffic density analysis, we provide a jupyter notebook called `marlin.ipynb` under `./analysis`. To ensure a working Python environment, we provide a `requirements.txt` file which can be used after creating a virtual environment for this project. To create a virtual environment within this directory and install the necessary packages, follow these instructions:

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## Code

After activating the virtual environment, you can run our main script using `python3 marlin.py`.

## Data

This directory contains the data we collected while evaluating our approach to detecting IMSI-Catchers.
