import amqp


class Worker:
    """
    A worker class to pull jobs off the given queue and process them.
    """

    def __init__(self, request_queue, result_queue, exchange='computome'):
        self.exchange = exchange
        self.requests = request_queue
        self.results = result_queue
        self.connection = None

    def _init_channel(self):
        """
        Establishes a connection to the worker's AMQP queue.
        """
        # Set up the connection.
        params = {
            'host': 'localhost:5672',
            'userid': 'worker',
            'password': 'worker',
            'virtual_host': '/',
            'insist': False,
        }
        self.connection = amqp.Connection(**params)
        self.channel = self.connection.channel()

    def _init_queues(self):
        """
        Initialises the request and result queues.
        """
        self.channel.exchange_declare(exchange=self.exchange, type='direct', durable=True, auto_delete=False)

        self.channel.queue_declare(queue=self.requests, durable=True, auto_delete=False)
        self.channel.queue_bind(queue=self.requests, exchange=self.exchange, routing_key='req')

        self.channel.queue_declare(queue=self.results, durable=True, auto_delete=False)
        self.channel.queue_bind(queue=self.results, exchange=self.exchange, routing_key='res')

    def handle_message(self, channel, method, properties, body):
        """
        Handles a message waiting on the incoming queue.

        :param channel: The name of the channel the message was on.
        :param method:
        :param properties:
        :param body: The contents of the message.
        """
        assert False
        print(" [x] Received %r, %s, %s, %s" % (body, channel, method, properties))
        result = self.process(body)

        msg = amqp.Message(result)
        msg.properties['delivery_mode'] = 2
        self.channel.basic_publish(msg, exchange=self.exchange, routing_key='res')

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

        print("Processing")
        self.channel.basic_consume(queue=self.requests, callback=self.handle_message, no_ack=True)
        print("Processed")
        self.connection.close()
