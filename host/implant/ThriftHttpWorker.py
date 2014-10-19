from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport

from models import ServiceLoader


class ThriftHttpWorker(object):
    def __init__(self, package):
        self.package = package

    def build_processor(self):
        loader = ServiceLoader('/mnt')
        service_class = loader.load_package('computome')[self.package]
        handler_class = loader.load_handler(self.package)
        return service_class.Processor(handler_class())

    def work(self):
        processor = self.build_processor()
        transport = TSocket.TServerSocket(port=9090)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

        print 'Starting the server...'
        try:
            server.serve()
        except Exception as e:
            print 'Server error: %s' % e
        print 'Server closed.'