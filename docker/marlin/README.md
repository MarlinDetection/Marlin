# Marlin Docker Image

This image operates under the assumptions that the host machine is (1) running Linux and (2) has the [UHD library](https://files.ettus.com/manual/page_install.html) installed and running to detect a USRP B210 SDR device connected locally via USB. We expect these to be true as we will pass the USB device files through to the container to connect our software to the necessary radio hardware. Please note that building this image may take several minutes to build due to the size of the UHD library.

## Build Image

We provide two options for building the image: (1) building from the Dockerfile within this repository, or (2) downloading a prebuilt image from Docker Hub.

```bash
# Build the container
docker build -t marlin .
```

If you prefer to download the Docker image directly from Docker Hub, please refer to this [Docker repository](https://hub.docker.com/repository/docker/tylermtucker/marlin/general). Use the command:

```bash
docker pull tylermtucker/marlin
```

## Run Container

```bash
# Start and attach to a container
docker run -it --privileged --device /dev/bus/usb/:/dev/bus/usb/ <image-name>
```

Where `image-name` is likely either `marlin` or `tylermtucker/marlin`, depending on which build instruction was used.

From within the container, you can access our main script directly.

```bash
# From the working directory of the container
./marlin.py -c marlin.ini
```
