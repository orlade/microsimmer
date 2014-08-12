from host.server.comm import ThriftClient


class RestServer:
    def invoke(self, service, request):
        client = ThriftClient(service)
        response = client.send(service, request)
        return response
