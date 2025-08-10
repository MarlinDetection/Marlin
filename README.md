# Detecting IMSI-Catchers by Characterizing Identity Exposing Messages in Cellular Traffic

This repository accompanies the publication *Detecting IMSI-Catchers by Characterizing Identity Exposing Messages in Cellular Traffic*. In this work, we introduce a new method for detecting rogue cellular base stations known as "IMSI-Catchers".

Our software operates under the assumptions that the host machine is (1) running Linux and (2) has the UHD library installed and running to detect a USRP B210 SDR device connected locally via USB. This is true whether the code is installed from source or running in a Docker container. For the latter case, we will pass the USB device files through to the container to connect our software to the necessary radio hardware.

### Overview

Our work first seeks to identify all messages that a (GSM/UMTS/LTE) base station can use to force a device to transmit its IMSI according to cellular standards, ultimately producing 53 unique "IMSI-exposing messages". We then create a new detection metric called the "IMSI-exposing ratio" that calculates the ratio of connections including at least one IMSI-exposing message to the total number of connections in a small time window. The theory behind this metric is that IMSI-Catchers *must* transmit one of these messages per device to operate, while legitimate base stations do not need to perform this operation for every connection. Furthermore, legitimate base stations will actively minimize the number of IMSI-exposing messages to protect the identifiers associated with the user.

### Repository

Our repository is organized as follows:

* `code` contains scripts for collecting new data, reproducing the results found in our paper, and analyzing new captures.
* `data` This directory contains the data we collected while evaluating our approach to detecting IMSI-Catchers. All captures can be analyzed using the programs provided in the `code/analysis` directory.
* `docker` provides two Dockerfiles to ease installation. The first, `marlin`, runs the Marlin detector using your own software-defined radios. The second, `marlin-data`, allows you to reproduce the results in our paper and plot new data without hardware requirements. To run our containers, you must have [Docker](https://docs.docker.com/engine/install/) installed on your machine.

Finally, please note that we provide a prebuilt [Docker image](https://hub.docker.com/repository/docker/tylermtucker/marlin/general) for download directly from Docker Hub. This can be used as an alternative to building an image from the Dockerfile provided within this repository.
