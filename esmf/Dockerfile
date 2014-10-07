FROM ubuntu:14.04

MAINTAINER Oliver Lade <piemaster21@gmail.com>
# See http://www.earthsystemmodeling.org/esmf_releases/public/last/ESMF_usrdoc/node6.html#SECTION00061000000000000000

# Install system dependencies.
RUN apt-get update
RUN apt-get install -qq g++ gfortran make
RUN apt-get install -qq git
RUN apt-get install -qq gcc
RUN apt-get install -qq openmpi-bin
RUN apt-get install -qq libopenmpi-dev
RUN apt-get install -qq wget


# Download the framework source.
RUN wget -q http://downloads.sourceforge.net/project/esmf/ESMF_6_3_0r/ESMF_6_3_0rp1/esmf_6_3_0rp1_src.tar.gz -O esmf.tar.gz
RUN tar xzf esmf.tar.gz -C /opt
RUN rm esmf.tar.gz


# Install dependencies.
ENV ESMF_PIO internal
ENV ESMF_NETCDF split
ENV ESMF_NETCDF_INCLUDE /opt/netcdf-4.3.2/include
ENV ESMF_NETCDF_LIBPATH /opt/netcdf-shared

RUN wget -q ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.2.tar.gz
RUN wget -q ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.4.1.tar.gz

RUN tar xzf netcdf-4.3.2.tar.gz -C /opt && rm netcdf-4.3.2.tar.gz
RUN tar xzf netcdf-fortran-4.4.1.tar.gz -C /opt && rm netcdf-fortran-4.4.1.tar.gz

RUN cd /opt/netcdf-4.3.2 && ./configure --disable-netcdf-4 && make
ENV CPPFLAGS -I/opt/netcdf-4.3.2/include
RUN cd /opt/netcdf-fortran-4.4.1 && ./configure && make

# Copy both NetCDF libraries to the same directory for ESMF linking.
RUN mkdir $ESMF_NETCDF_LIBPATH
RUN cp /opt/netcdf-4.3.2/liblib/.libs/libnetcdf.so $ESMF_NETCDF_LIBPATH
RUN cp /opt/netcdf-fortran-4.4.1/fortran/.libs/libnetcdff.so $ESMF_NETCDF_LIBPATH
RUN cp /opt/netcdf-fortran-4.4.1/fortran/netcdf.mod $ESMF_NETCDF_LIBPATH


# Install the framework.
ENV ESMF_DIR /opt/esmf
ENV ESMF_COMM openmpi

# ENV ESMF_INSTALL_PREFIX $ESMF_DIR/install
# ENV ESMF_INSTALL_LIBDIR $ESMF_INSTALL_PREFIX/lib
ENV ESMFMKFILE $ESMF_DIR/lib/libO/Linux.gfortran.64.openmpi.default/esmf.mk

RUN cd $ESMF_DIR && make -s -w
# Check the 
# RUN cd $ESMF_DIR && make -s -w installcheck

# Install the application.
ADD install/ESMF_CoupledFlow.tar.gz /opt/
RUN cd /opt/ESMF_CoupledFlow && make -s -w

# Install Python to run worker scripts.
RUN apt-get install -qq python

# Copy the API directory across.
ADD api /api

# Ensure the installation works. If this call fails, the whole build will fail.
RUN mpirun -np 4 /opt/ESMF_CoupledFlow/ESMF_CoupledFlow
