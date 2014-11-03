FROM python:2.7.8

MAINTAINER Oliver Lade <oliver@runsimmer.com>

ENV SIMMER_HOME /opt/microsimmer

ADD host $SIMMER_HOME/
ADD serve.py $SIMMER_HOME/
ADD requirements.txt $SIMMER_HOME/

RUN pip install -r $SIMMER_HOME/requirements.txt

EXPOSE 5000

ENTRYPOINT $SIMMER_HOME/serve.py
