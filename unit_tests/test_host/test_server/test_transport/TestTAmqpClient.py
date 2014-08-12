from host.server.transport.TAmqpClient import TAmqpClient

from unit_tests.util import *
from unit_tests.MockChannel import build_mock_channel, populate


class TestTAmqpClient():
    def __init__(self):
        self.client = None
        self.channel = None

    def setup(self):
        self.channel = build_mock_channel()
        self.client = TAmqpClient(TEST_EXCHANGE, TEST_REQUEST_QUEUE, channel=self.channel)

    def test_isOpen(self):
        assert_that(self.client.isOpen(), equal_to(False))
        self.client.open()
        assert_that(self.channel.open.assert_called_once())

    def test_open(self):
        self.client.open()
        assert_that(self.channel.open.assert_called_once())

    def test_close(self):
        self.client.open()
        self.client.close()
        assert_that(self.channel.close.assert_called_once())
        assert_that(self.channel.open.assert_called_once())

    def test_read(self):
        body = 'Foo'
        populate([amqp.Message(body)])
        self.client.open()
        assert_that(self.client.read().body, equal_to(body))

    def test_readAll(self):
        pass

    def test_write(self):
        self.client.write('Foo')
        assert_that(self.client._TAmqpClient__wbuf.getvalue(), equal_to('Foo'))


    def test_flush(self):
        self.client.open()
        body = 'Foo'
        self.client.write(body)
        msg = self.client.flush()
        self.channel.basic_publish.assert_called_once_with(
            msg, exchange=TEST_EXCHANGE, routing_key=TEST_REQUEST_QUEUE)