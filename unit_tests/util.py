from hamcrest import *
import amqp

TEST_EXCHANGE = 'test.computome'
TEST_REQUEST_QUEUE = 'test.computome.request'
TEST_RESULT_QUEUE = 'test.computome.result'

AMQP_PARAMS = {
    'host': 'localhost:5672',
    'userid': 'test',
    'password': 'test',
    'virtual_host': '/',
    'insist': False,
}

# Connect to AMQP and create the channel.
connection = amqp.Connection(**AMQP_PARAMS)
channel = connection.channel()

# Set up the test request and result queues on the test exchange.
channel.exchange_declare(exchange=TEST_EXCHANGE, type='direct', durable=True, auto_delete=False)
channel.queue_declare(queue=TEST_REQUEST_QUEUE, durable=True, auto_delete=False)
channel.queue_bind(queue=TEST_REQUEST_QUEUE, exchange=TEST_EXCHANGE, routing_key='req')
channel.queue_declare(queue=TEST_RESULT_QUEUE, durable=True, auto_delete=False)
channel.queue_bind(queue=TEST_RESULT_QUEUE, exchange=TEST_EXCHANGE, routing_key='res')


def publish_message(body='Hello, World!'):
    msg = amqp.Message(body)
    msg.properties['delivery_mode'] = 2
    channel.basic_publish(msg, exchange=TEST_EXCHANGE, routing_key='req')


def count_messages(queue):
    return channel.queue_declare(queue=queue, passive=True)[1]


def assert_queue_size(sizes):
    """
    Ensures that all queues contain the expected number of messages.
    :param sizes: A map of queue names to the expected number of messages in the queue.
    """
    for queue in sizes:
        assert_that(count_messages(queue), is_(sizes[queue]))