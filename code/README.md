# Marlin Code

This guide assumes that you have Python 3 installed on your system. If you do not, please follow this [guide](https://realpython.com/installing-python/).

### Installation

We provide a `requirements.txt` file that can be used with a local Python virtual environment to install dependencies for all of our scripts.

```bash
python3 -m venv ./venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```

To reactivate the virtual environment in future sessions, run the `source ./venv/bin/activate` command from this directory.

### Analysis

All of our scripts for analyzing cellular network traffic are found in this directory. All code can be run using a Python 3 environment and does not require specialized hardware.

### Marlin Tool

This directory contains the `marlin.py` analysis tool that allows you to analyze cellular traffic in real time. This tool has specialized hardware requirements, namely a software-defined radio attached to the host machine.

You need at least one software-defined radio (SDR) supported by srsRAN to run LTE analysis and at least one SDR supported by gr-gsm to run GSM analysis. We confirmed that our LTE code works with the [Ettus Research USRP B210](https://www.ettus.com/all-products/ub210-kit/).
