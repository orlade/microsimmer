from unit_tests.util import *
from unit_tests.test_host.test_implant.TestWorker import TestWorker

from host.implant.ThriftWorker import ThriftWorker


class TestThriftWorker(TestWorker):

    def setup(self):
        self.worker = ThriftWorker(TEST_REQUEST_QUEUE, TEST_RESULT_QUEUE, TEST_EXCHANGE)

    def test_work_manual(self):
        publish_message('Foo')
        publish_message('Bar')

        while True:
            message = channel.basic_get(TEST_REQUEST_QUEUE)
            print("Got ", message)
            if message is not None:
                self.worker.process(message.body)
            else:
                break
        assert_queue_size({TEST_REQUEST_QUEUE: 0, TEST_RESULT_QUEUE: 2})