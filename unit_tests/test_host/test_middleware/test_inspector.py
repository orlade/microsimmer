import sys

sys.path.append('../../..')
sys.path.append('/var/computome/pie21_sumo/gen-py/services')

from host.middleware.inspector import *
import SumoService

def test_get_thrift_methods():
    cls = SumoService
    print cls
    print get_thrift_methods(cls)

if __name__ == '__main__':
    test_get_thrift_methods()