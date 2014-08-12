from thrift.protocol import TBinaryProtocol
from thrift.protocol.TJSONProtocol import TJSONProtocol
from thrift.transport.TTransport import TMemoryBuffer
from host.server.transport import TAmqpClient


class ThriftBuilder:
    def __init__(self):
        pass

    def convert_json(self, json):
        iprot = TBinaryProtocol(TAmqpClient())
        iprot = TJSONProtocol(TMemoryBuffer(json))
        oprot = TJSONProtocol(TMemoryBuffer())

        # MyLoginHandler defines "login(username, password): SessionKey"
        processor = meta.build_processor(service)
        processor.process(iprot, oprot)
        print oprot.trans.getvalue()