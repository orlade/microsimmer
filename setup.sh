# Install Thrift and Docker.
sudo apt-get install -qq thrift-compiler docker.io

# Run the microSimmer image and serve to port 80.
sudo docker run -p 80:5000 orlade/microsimmer
