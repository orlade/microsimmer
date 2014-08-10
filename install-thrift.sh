# Compiles and installs Apache Thrift v0.9.1 from source.

cwd=$(pwd)
version='0.9.1'

wget http://mirror.ventraip.net.au/apache/thrift/$version/thrift-$version.tar.gz -O /tmp/thrift-$version.tar.gz
cd /tmp
tar -zxf thrift-$version.tar.gz
cd thrift-$version
./configure && sudo make install

cd lib/py
sudo make install

cd $wd
