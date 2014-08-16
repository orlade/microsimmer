# Information about the service.

import sys
sys.path.append('gen-py')

from services import SumoService
from handler import SumoServiceHandler

def get_id():
    return 'sumo'

# The Docker image with SUMO installed.
def get_image():
    return 'pie21/sumo-manual'

command = 'sumo'

services = {
    'sumo': {
        'service': SumoService,
        'client': SumoService.Client,
        'processor': SumoService.Processor,
        'handler': SumoServiceHandler,
    },
}

def build_client(service_name):
    return services[service_name]['client'](services[service_name]['service'].Iface)

def build_handler(service_name):
    return services[service_name]['handler']()
    
def build_processor(service_name):
    handler = build_handler(service_name)
    return services[service_name]['processor'](handler)
