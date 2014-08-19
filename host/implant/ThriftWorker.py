from Worker import Worker

# TODO(orlade): Clean up imports.
from models import ServiceLoader
from handler import SumoServiceHandler

from thrift.transport.TTransport import TMemoryBuffer
from thrift.protocol.TBinaryProtocol import TBinaryProtocol


class ThriftWorker(Worker):
    def __init__(self, request_queue, result_queue, exchange='computome'):
        super(ThriftWorker, self).__init__(request_queue, result_queue, exchange)
        self.exchange = exchange
        self.requests = request_queue
        self.results = result_queue

    def build_processor(self):
        handler = SumoServiceHandler()

        # TODO(orlade): Make variable.
        service_name = 'SumoService'
        loader = ServiceLoader('/mnt')
        service = loader.load_package('computome')[service_name]
        return service.Processor(handler)

    def process(self, body):
        """
        Processes the body of the message as a Thrift request through a processor.
        :param body: The content of the Thrift request.
        :return: The result of the calculation in a Thrift message.
        """

        # Create a protocol to read/write messages from/to AMQP.
        iprot = TBinaryProtocol(TMemoryBuffer(body))
        oprot = TBinaryProtocol(TMemoryBuffer())
        # Process messages from AMQP and put the results back on the result queue.
        self.processor.process(iprot, oprot)

        return oprot.trans.getvalue()