"""
Simple interface to create a Worker to processes AMQP messages.
"""
# TODO(orlade): Customise queues with metadata about service.

import sys
sys.path.append('/api')

from host.implant.ThriftWorker import ThriftWorker

if __name__ == '__main__':
    ThriftWorker('computome.request', 'computome.result').work()