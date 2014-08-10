import sys
sys.path.append('gen-py')

import meta
import util

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:

    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = meta.build_client('sumo')

    transport.open()

    network = util.read_file('eichstaett.net.xml')
    xml = client.randomDayHourly(network)
    print 'output = %s' % (xml)

    transport.close()

except Thrift.TException, tx:
    print '%s' % (tx.message)
