from host.server.transport.TAmqpClient import TAmqpClient
from unit_tests.util import *


class TestTAmqpClient():
    def setup(self):
        self.client = TAmqpClient(AMQP_PARAMS, TEST_EXCHANGE, TEST_REQUEST_QUEUE)

    def teardown(self):
        purge_test_queues()

    def test_isOpen(self):
        assert not self.client.isOpen()
        self.client.open()
        assert self.client.isOpen()

    def test_open(self):
        self.client.open()
        assert self.client.isOpen()

    def test_close(self):
        self.client.open()
        assert_that(self.client.isOpen())
        self.client.close()
        assert_that(is_not(self.client.isOpen()))

    def test_read(self):
        self.client.open()
        body = 'Foo'
        publish_message(body)
        msg = self.client.read()
        assert_that(msg.body, equal_to(body))

    def test_readAll(self):
        pass

    def test_write(self):
        self.client.open()
        body = 'Foo'
        self.client.write(body)
        assert_that(channel.basic_get(queue=self.client.queue).body, equal_to(body))

    def test_flush(self):
        pass