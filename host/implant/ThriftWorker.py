from host.implant.Worker import Worker

from sumo.api import meta

from thrift.transport.TTransport import TMemoryBuffer
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

class ThriftWorker(Worker):

    def __init__(self, request_queue, result_queue, exchange='computome'):
        super(Worker, self).__init__()
        self.exchange = exchange
        self.requests = request_queue
        self.results = result_queue
        self.connection = None

        self.processor = meta.build_processor('sumo')

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