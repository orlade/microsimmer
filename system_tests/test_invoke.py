import bottle

from host.server.rest import RestServer


def test_invoke():
    server = RestServer()

    server.register_package('pie21/sumo')

    arguments = [{'arguments': '--help'}]

    server.invoke('pie21/sumo', 'SumoService', 'call', arguments)