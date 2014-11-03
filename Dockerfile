FROM python:2.7.8-onbuild

MAINTAINER Oliver Lade <oliver@runsimmer.com>

# Install Thrift and Docker inside the container.
RUN apt-get update && apt-get install -qq thrift-compiler docker.io

# Expose Bottle's listen port.
EXPOSE 5000

# Start the Bottle server.
CMD ["python", "./serve.py"]
