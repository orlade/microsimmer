import bottle

from host.server.rest import RestServer


def test_invoke():
    server = RestServer()

    server.register_package('pie21/sumo-manual')

    arguments = [{'arguments': '--help'}]

    server.invoke('pie21/sumo-manual', 'SumoService', 'call', arguments)