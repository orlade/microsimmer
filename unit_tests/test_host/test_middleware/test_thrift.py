import subprocess
import sys
sys.path.append('../../..')
sys.path.append('../../../host/system')
sys.path.append('../../../sumo/api')
sys.path.append('../../../sumo/api/gen-py/services')

import time

from host.implant.ThriftHttpWorker import ThriftHttpWorker
from host.middleware.comms.ThriftHttpClient import ThriftHttpClient

import SumoService

this_path = 'C:/dev/workspace/computome/unit_tests/test_host/test_middleware/test_thrift.py'
xml_path = 'C:\dev\workspace\computome\sumo\example\eichstaett.net.xml'

def test_send_receive():

    subprocess.Popen(['python', this_path])

    time.sleep(1)

    print 'Starting client...'
    client = ThriftHttpClient(SumoService)

    client.send('call', [{}])
    print 'ping()'

    with open(xml_path, 'r') as f:
        xml = f.read()
        result = client.send('randomDayHourly', [xml])

    assert result

if __name__ == '__main__':
    worker = ThriftHttpWorker(SumoService).work()
    time.sleep(1)