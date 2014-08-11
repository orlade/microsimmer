from unit_tests.util import *
from unit_tests.AmqpTestCase import AmqpTestCase

from host.implant.Worker import Worker


class TestWorker(AmqpTestCase):
    """
    Tests the functionality of the Worker class to process AMQP messages.
    """

    def __init__(self):
        self.worker = None

    def setup(self):
        self.worker = Worker(TEST_REQUEST_QUEUE, TEST_RESULT_QUEUE, TEST_EXCHANGE)

    def test_create(self):
        """
        Tests that a Worker can be created.
        """
        assert self.worker.connection is None or self.worker.connection.is_alive()
        assert_queue_size({TEST_REQUEST_QUEUE: 0, TEST_RESULT_QUEUE: 0})

    def test_work(self):
        """
        Tests that a Worker can process a message and produce a result.
        """
        publish_message('Foo')
        publish_message('Bar')
        self.worker.work()
        assert_queue_size({TEST_REQUEST_QUEUE: 0, TEST_RESULT_QUEUE: 2})