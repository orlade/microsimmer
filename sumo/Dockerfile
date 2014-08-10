FROM ubuntu

MAINTAINER Oliver Lade <piemaster21@gmail.com>

RUN sudo apt-get update
RUN sudo apt-get install software-properties-common
RUN sudo add-apt-repository ppa:sumo/stable
RUN sudo apt-get update

RUN apt-get -qq install sumo sumo-tools sumo-doc ruby-dev libssl-dev
RUN gem install puma

RUN echo "run Proc.new { |env| ['200', {'Content-Type' => 'text/html'}, ['get rack\'d']] }" >> /opt/config.ru
