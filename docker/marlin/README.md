# Marlin Docker Image

Please note that building this image may take several minutes to build due to the size of the UHD library. Additionally, we must mount the device directory of the host machine to access the software-defined radios from within the container. Note that the host machine must have the [UHD library](https://files.ettus.com/manual/page_install.html) installed to ensure that USRP devices can be found.

```bash
# Build the container
docker build -t marlin .
# Start and attach to a container
docker run -it --privileged --device /dev/bus/usb/:/dev/bus/usb/ marlin
```

From within the container, you can access our main script directly.

```bash
# From the working directory of the container
./marlin.py -c marlin.ini
```
