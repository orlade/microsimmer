import sys
sys.path.append('../../..')
sys.path.append('../../../host/system')
sys.path.append('../../../sumo/api')

from host.implant.network import *
from host.implant.ThriftWorker import ThriftWorker
from host.middleware.comm import ThriftClient

def test_send_receive():
    channel = amqp_connect()
    client = ThriftClient('sumo')
    worker = ThriftWorker(REQUESTS_QUEUE, RESULTS_QUEUE)

    result = client.send('randomDayHourly', '')
    # server = build_server(channel, proc)

if __name__ == '__main__':
    test_send_receive()