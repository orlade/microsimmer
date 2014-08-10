# A Thrift server to expose the service handler methods.

import sys
import meta

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TJSONProtocol
from thrift.server import TServer


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Insufficient arguments (requires service name)')

    service = sys.argv[1]
    json = None
    if len(sys.argv) > 2:
        json = sys.argv[2]
    
    iprot = TJSONProtocol.TJSONProtocol(TTransport.TMemoryBuffer(json))
    oprot = TJSONProtocol.TJSONProtocol(TTransport.TMemoryBuffer())
 
    # MyLoginHandler defines "login(username, password): SessionKey"
    processor = meta.build_processor(service)
    processor.process(iprot, oprot)
    print oprot.trans.getvalue()
