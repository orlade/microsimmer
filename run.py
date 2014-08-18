from host.server import facade
from host.server.rest import RestServer

if __name__ == '__main__':
    #facade.init()

    server = RestServer()

    server.register_package('pie21/sumo')

    arguments = [{'--help': ''}]

    server.invoke('pie21/sumo', 'SumoService', 'call', arguments)
