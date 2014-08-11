from unit_tests.util import *


class AmqpTestCase:
    """
    Tests the functionality of a component that uses AMQP message queues.

    Ensures that the message queues are purged afetr each test.
    """

    def teardown(self):
        """
        Purges the test queues.
        """
        purge_test_queues()
