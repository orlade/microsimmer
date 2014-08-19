import os

import amqplib.client_0_8 as amqp
from network import RESULT_KEY, EXCHANGE, build_server
from network import amqp_connect


class Worker(object):
    """
    A worker class to pull jobs off the given queue and process them.
    """

    def __init__(self, request_queue, result_queue, exchange=EXCHANGE):
        print('Initialising worker for %s' % request_queue)
        self.exchange = exchange
        self.requests = request_queue
        self.results = result_queue
        # Set in sublcass.
        self.processor = self.build_processor()
        self.channel = amqp_connect()

    def build_processor(self):
        """
        Creates a service Processor object to use in the server.
        :return: The created Processor.
        """
        return None

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
        self.channel.basic_publish(msg, exchange=EXCHANGE, routing_key=RESULT_KEY)
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
        server = build_server(self.channel, self.processor)

        print 'Starting the server...'
        server.serve()
        print 'Serve finished'
