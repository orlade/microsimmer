import os
import amqplib.client_0_8 as amqp
from amqplib_thrift.factories import TAMQInputTransportFactory, TAMQOutputTransportFactory
from amqplib_thrift.transports import TAMQTransport, TAMQServerTransport
from thrift.protocol.TBinaryProtocol import TBinaryProtocolFactory
from thrift.server.TServer import TSimpleServer

CONNECTION_PARAMS = {
    'host': '%s:%d' % (os.environ.get('MQ_PORT_5672_TCP_ADDR', '172.17.0.2'), 5672),
    'userid': 'guest',
    'password': 'guest',
    'virtual_host': '/',
    'insist': False,
}

EXCHANGE = 'computome'
REQUESTS_QUEUE = 'computome.req'
RESULTS_QUEUE = 'computome.res'
REQUEST_KEY = 'req'
RESULT_KEY = 'res'


def amqp_connect():
    print('Connecting to AMQP on %s' % CONNECTION_PARAMS)
    connection = amqp.Connection(**CONNECTION_PARAMS)
    channel = connection.channel()

    # Declare the queues.
    channel.exchange_declare(exchange=EXCHANGE, type='direct', durable=True, auto_delete=False)

    channel.queue_declare(queue=REQUESTS_QUEUE, durable=True, auto_delete=False)
    channel.queue_bind(queue=REQUESTS_QUEUE, exchange=EXCHANGE, routing_key=REQUEST_KEY)
    channel.queue_bind(queue=REQUESTS_QUEUE, exchange=EXCHANGE, routing_key=REQUESTS_QUEUE)

    channel.queue_declare(queue=RESULTS_QUEUE, durable=True, auto_delete=False)
    channel.queue_bind(queue=RESULTS_QUEUE, exchange=EXCHANGE, routing_key=RESULT_KEY)
    # Bind to the queue name so TAMQTransport's reply_to property is received.
    channel.queue_bind(queue=RESULTS_QUEUE, exchange=EXCHANGE, routing_key=RESULTS_QUEUE)

    return channel


def build_req_transport(channel):
    """
    Creates a TAMQTransport for service requests.
    :return: The created transport.
    """
    # Note: The queue kwarg actually specifies the routing key that the response will be marked with.
    return TAMQTransport(channel, EXCHANGE, REQUEST_KEY, queue=RESULTS_QUEUE)


def build_server(channel, processor):
    # Create incoming request transport.
    treq = TAMQServerTransport(channel, REQUESTS_QUEUE)

    itfactory = TAMQInputTransportFactory()
    otfactory = TAMQOutputTransportFactory(channel, EXCHANGE)
    pfactory = TBinaryProtocolFactory()

    server = TSimpleServer(processor, treq, itfactory, otfactory, pfactory, pfactory)
    # TODO(orlade): Use one of these in production:
    # server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    return server