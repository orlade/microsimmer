import os
from amqplib_thrift.factories import TAMQOutputTransportFactory, TAMQInputTransportFactory
from thrift.transport.TSocket import TSocket
from thrift.server import TServer

import amqplib.client_0_8 as amqp
from amqplib_thrift.transports import TAMQTransport, TAMQServerTransport
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport


class Worker:
    """
    A worker class to pull jobs off the given queue and process them.
    """

    def __init__(self, request_queue, result_queue, exchange='computome'):
        print('Initialising worker for %s' % request_queue)
        self.exchange = exchange
        self.requests = request_queue
        self.results = result_queue
        self.connection = None
        # Set in sublcass.
        self.processor = None

    def _init_channel(self):
        """
        Establishes a connection to the worker's AMQP queue.
        """
        # Set up the connection.
        # TODO(orlade): Extract details to environment.
        params = {
            'host': '%s:%d' % (os.environ.get('MQ_PORT_5672_TCP_ADDR', '172.17.0.2'), 5672),
            'userid': 'guest',
            'password': 'guest',
            'virtual_host': '/',
            'insist': False,
        }
        print('Connecting container to AMQP on %s' % params)
        self.connection = amqp.Connection(**params)
        self.channel = self.connection.channel()

    def _init_queues(self):
        """
        Initialises the request and result queues.
        """
        # TODO(orlade): Extract details to environment.
        self.channel.exchange_declare(exchange=self.exchange, type='direct', durable=True, auto_delete=False)

        self.channel.queue_declare(queue=self.requests, durable=True, auto_delete=False)
        self.channel.queue_bind(queue=self.requests, exchange=self.exchange, routing_key='req')

        self.channel.queue_declare(queue=self.results, durable=True, auto_delete=False)
        self.channel.queue_bind(queue=self.results, exchange=self.exchange, routing_key='res')

    def handle_message(self, msg):
        """
        Handles a message waiting on the incoming queue.

        :param msg: The message received.
        """
        print('Processing message: "%s"' % msg.body)
        result = self.process(msg.body)
        print('Computed result: %s' % str(result))

        msg = amqp.Message(result)
        msg.properties['delivery_mode'] = 2
        self.channel.basic_publish(msg, exchange=self.exchange, routing_key='res')
        self.channel.basic_cancel('work')

    def process(self, body):
        """
        Processes the given messages and returns a result value.
        :param body: The body of the message to process.
        :return: The result of processing the message body.
        """
        raise NotImplementedError("Please implement this method in a Worker subclass")

    def work(self):
        """
        Starts the worker consuming messages from the incoming queue.
        :return:
        """
        self._init_channel()
        self._init_queues()


        # Create incoming request transport.
        treq = TAMQServerTransport(self.channel, self.requests)

        itfactory = TAMQInputTransportFactory()
        otfactory = TAMQOutputTransportFactory(self.channel, self.exchange)
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TSimpleServer(self.processor, treq, itfactory, otfactory, pfactory, pfactory)

        # You could do one of these for a multithreaded server
        # server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
        #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

        print 'Starting the server...'
        server.serve()
        print 'done.'

        # self.processor
        #
        # self.client = service_class.Client(req_prot)

        # self.channel.basic_consume(queue=self.requests, callback=self.handle_message, no_ack=True, consumer_tag='work')
        #
        # import time
        # t = 0
        # clock = time.time()
        # while t < 3:
        #     print('Waiting to consume (t = %d)' % t)
        #     self.channel.wait()
        #     t = time.time() - clock
        #     time.sleep(1)
        #     print('Nom (t = %d)' % t)
        # #self.connection.close()
