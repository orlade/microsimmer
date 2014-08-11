from host.server.transport.TAmqpClient import TAmqpClient
from unit_tests.util import *

params = {
    'host': 'localhost:5672',
    'userid': 'worker',
    'password': 'worker',
    'virtual_host': '/',
    'insist': False,
}


class TestTAmqpClient:
    def setup(self):
        self.client = TAmqpClient(params, TEST_EXCHANGE, TEST_REQUEST_QUEUE)


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
        pass

    def test_readAll(self):
        pass

    def test_write(self):
        pass

    def test_flush(self):
        pass