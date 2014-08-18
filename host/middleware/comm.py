import os

from amqplib.client_0_8.connection import Connection
from amqplib_thrift.transports import TAMQTransport, TAMQServerTransport
from thrift.protocol.TBinaryProtocol import TBinaryProtocol


class ThriftServer:
    pass


class ThriftClient:
    def __init__(self, service_class):
        self.service_class = service_class

        # TODO(orlade): Inject this in config.
        exchange = 'computome'
        req_queue = 'computome.req'
        res_queue = 'computome.res'

        amqp_params = {
            'host': '%s:%d' % (os.environ.get('MQ_PORT_5672_TCP_ADDR', '172.17.0.2'), 5672),
            'userid': 'guest',
            'password': 'guest',
            'virtual_host': '/',
            'insist': False,
        }
        print('Connecting client to AMQP on %s, %s => %s' % (amqp_params, req_queue, res_queue))

        # Open an AMQP channel.
        connection = Connection(**amqp_params)
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange, type='direct', durable=True, auto_delete=False)

        channel.queue_declare(queue=req_queue, durable=True, auto_delete=False)
        channel.queue_bind(queue=req_queue, exchange=exchange, routing_key='req')

        channel.queue_declare(queue=res_queue, durable=True, auto_delete=False)
        channel.queue_bind(queue=res_queue, exchange=exchange, routing_key='res')

        # Create transports.
        # Note: The queue kwarg actually specifies the routing key that the response will be marked with.
        self.__treq = TAMQTransport(channel, exchange, 'req', queue=res_queue)

        # Create protocols.
        req_prot = TBinaryProtocol(self.__treq)

        self.client = service_class.Client(req_prot)

    # TODO(orlade): Allow map of keyword arguments instead, parse from JSON.
    def send(self, method_name, arguments):
        """
        Uses the client to invoke the target method with the given arguments.

        :param method_name: The name of the method of the client to invoke.
        :param arguments: The arguments (positional list) to pass to the client method.
        :return: The response from the client.
        """
        method = getattr(self.client, method_name)
        # TODO(orlade): Fix blocking breaking tests.
        if arguments is None:
            print(' >> Calling Thrift service method "%s" with no arguments' % method_name)
            method()
        else:
            print(' >> Calling Thrift service method "%s" with arguments %s' % (method_name, arguments))
            return method(*arguments)