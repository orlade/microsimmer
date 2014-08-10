FROM ubuntu:14.04

MAINTAINER Oliver Lade <piemaster21@gmail.com>
# See http://sumo-sim.org/userdoc/Installing/Linux_Build.html

RUN apt-get update
RUN apt-get install -qq wget g++ make libxerces-c3.1 libxerces-c3-dev

RUN wget http://downloads.sourceforge.net/project/sumo/sumo/version%200.21.0/sumo-src-0.21.0.tar.gz -O sumo-src-0.21.0.tar.gz
RUN tar xzf sumo-src-0.21.0.tar.gz
RUN cd sumo-0.21.0 && ./configure
RUN cd sumo-0.21.0 && make install
RUN sumo
