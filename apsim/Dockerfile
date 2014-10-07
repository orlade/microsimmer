FROM ubuntu:14.04

MAINTAINER Oliver Lade <piemaster21@gmail.com>

RUN apt-get update

# Install dependencies.
RUN apt-get -qq install g++ gfortran
RUN apt-get -qq install mono-devel mono-vbnc
RUN apt-get -qq install libboost-all-dev
RUN apt-get -qq install libxml2-dev
RUN apt-get -qq install tcl8.5-dev
RUN apt-get -qq install r-recommended
RUN apt-get -qq install subversion

# Install R package dependencies.
COPY ./install-packages.r /tmp/install-packages.r
RUN chmod +x /tmp/install-packages.r
RUN /tmp/install-packages.r

# Checkout APSIM source code.
RUN svn checkout http://apsrunet.apsim.info/svn/apsim/trunk /opt/apsim

# Build APSIM from source.
RUN chmod +x /opt/apsim/Model/Build/CleanAll.sh
RUN chmod +x /opt/apsim/Model/Build/BuildAll.sh
RUN cd /opt/apsim/Model/Build && ./CleanAll.sh && ./BuildAll.sh

# Run the main binary to ensure it exists.
RUN apsim

