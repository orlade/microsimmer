from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from models import ServiceLoader
from handler import SumoServiceHandler
from thrift.transport import TSocket, TTransport


class ThriftHttpWorker(object):
    def __init__(self, service_class):
        self.service_class = service_class

    def build_processor(self):
        handler = SumoServiceHandler()
        return self.service_class.Processor(handler)

    def work(self):
        processor = self.build_processor()
        transport = TSocket.TServerSocket(port=9090)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

        print 'Starting the server...'
        server.serve()
        print 'Server closed.'