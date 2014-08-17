import amqplib.client_0_8 as amqp


class Experiment:
    """
    A worker class to pull jobs off the given queue and process them.
    """

    def __init__(self, request_queue, result_queue, exchange='computome'):
        print('Initialising worker for %s' % request_queue)
        self.exchange = exchange
        self.requests = request_queue
        self.results = result_queue
        self.connection = None

        # Set up the connection.
        params = {
            'host': '172.17.0.2:5672',
            'userid': 'guest',
            'password': 'guest',
            'virtual_host': '/',
            'insist': False,
        }
        self.connection = amqp.Connection(**params)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, type='direct', durable=True, auto_delete=False)

        self.channel.queue_declare(queue=self.requests, durable=True, auto_delete=False)
        self.channel.queue_bind(queue=self.requests, exchange=self.exchange, routing_key='req')

        self.channel.queue_declare(queue=self.results, durable=True, auto_delete=False)
        self.channel.queue_bind(queue=self.results, exchange=self.exchange, routing_key='res')

        print self.channel.basic_get(request_queue)
        msg = amqp.Message('hello')
        print self.channel.basic_publish(msg, exchange, 'req')
        print ('done')

if __name__ == '__main__':
    Experiment('computome.req', 'computome.res')