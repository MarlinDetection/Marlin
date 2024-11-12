FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York
ENV USB_GROUP=usbusers
ENV USB_GID=10001
ARG MAKEWIDTH=2

# Download UHD dependencies
RUN apt-get update
RUN	apt-get install -y autoconf automake build-essential ccache cmake cpufrequtils doxygen ethtool g++ git inetutils-tools libboost-all-dev libncurses5 libncurses5-dev libusb-1.0-0 libusb-1.0-0-dev libusb-dev python3-dev python3-mako python3-numpy python3-requests python3-scipy python3-setuptools python3-ruamel.yaml tshark

# Ensure that we start in the home directory
RUN cd $HOME

# Clone and build UHD from source
RUN          mkdir -p /usr/local/src
RUN          git clone https://github.com/EttusResearch/uhd.git /usr/local/src/uhd
RUN          cd /usr/local/src/uhd/
RUN          mkdir -p /usr/local/src/uhd/host/build
WORKDIR      /usr/local/src/uhd/host/build
RUN			 git checkout UHD-4.7
RUN          cmake .. -DENABLE_PYTHON_API=ON
RUN          make -j $MAKEWIDTH
RUN          make install
RUN          uhd_images_downloader
WORKDIR      /

# Download srsRAN dependencies
RUN apt-get install -y build-essential git cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev

# Download LTESniffer dependencies
RUN apt-get install -y libglib2.0-dev libudev-dev libcurl4-gnutls-dev libboost-all-dev qtdeclarative5-dev libqt5charts5-dev 
RUN ls -a

# Build LTESniffer from source
RUN git clone https://github.com/SysSec-KAIST/LTESniffer.git
RUN	cd LTESniffer
RUN	mkdir build
RUN	cd build
WORKDIR /LTESniffer/build
RUN	cmake ../
RUN	make -j $MAKEWIDTH

# Ensure that we start in the home directory
RUN cd $HOME
WORKDIR /

# Download Marlin dependencies
RUN apt -y install python3-venv python3-pip pcapfix

# Get Marlin code
RUN git clone https://github.com/MarlinDetection/Marlin
RUN cd Marlin/code
WORKDIR /Marlin/code
RUN	python3 -m venv ./venv
RUN /bin/bash -c 'source ./venv/bin/activate'
RUN	python3 -m pip install -r requirements.txt
WORKDIR /Marlin/code/marlin

# Enable USB passthrough
RUN apt install -y avahi-daemon avahi-utils dbus
RUN groupadd --gid "${USB_GID}" "${USB_GROUP}"

# Automatically start USB passthrough on boot
RUN echo "service dbus start" >> /root/.bashrc
RUN echo "service avahi-daemon start" >> /root/.bashrc
