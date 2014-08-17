"""
Simple interface to create a Worker to processes AMQP messages.
"""
# TODO(orlade): Customise queues with metadata about service.

import sys
import time

sys.path.append('/api')
sys.path.append('/mnt/computome')
sys.path.append('/mnt/computome/gen-py')

from ThriftWorker import ThriftWorker

""" Number of seconds to wait before processing the queue (allow time for publish). """
DELAY = 1

if __name__ == '__main__':
    print('Starting worker for computome.request in %d secs...' % DELAY)
    time.sleep(DELAY)
    ThriftWorker('computome.req', 'computome.res').work()