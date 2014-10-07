"""
Simple interface to create a Worker to processes incoming requests.
"""
import sys
import time

sys.path.append('/api')
sys.path.append('/mnt/computome')
sys.path.append('/mnt/computome/gen-py')

from ThriftHttpWorker import ThriftHttpWorker

""" Number of seconds to wait before processing the queue (allow time for publish). """
DELAY = 1

if __name__ == '__main__':
    print('Starting worker for computome.request in %d secs...' % DELAY)
    time.sleep(DELAY)
    ThriftHttpWorker('computome.req', 'computome.res').work()