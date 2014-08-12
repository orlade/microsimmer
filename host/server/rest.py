from host.server.comm import ThriftClient
from host.server.registry import Registry


class RestServer:

    def __init__(self):
        self.registry = Registry()

    def register(self, service, image_id):
        # TODO(orlade): Get ServiceClass from image_id.
        self.registry.register(service, image_id)

    def unregister(self, service):
        self.registry.unregister(service)

    def invoke(self, service, request):
        client = ThriftClient(service)
        response = client.send(service, request)
        return response
