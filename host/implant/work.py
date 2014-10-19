"""
Simple interface to create a Worker to processes incoming requests.
"""
import sys

sys.path.append('/api')
sys.path.append('/mnt/computome')
sys.path.append('/mnt/computome/gen-py')

from ThriftHttpWorker import ThriftHttpWorker

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Expecting package name as sys.argv[1]')

    package = sys.argv[1]
    print 'Starting worker for %s...' % package
    ThriftHttpWorker(package).work()