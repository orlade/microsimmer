import bottle
from bottle import get, post, delete, request

from host.server.comm import ThriftClient
from host.server.registry import Registry
from host.system.docker import ComputomeContainer


class RestServer:
    def __init__(self):
        self.registry = Registry()

    @post('/services/register')
    def register_package(self):
        """
        Registers a package to a Docker image ID. The request should contain a "docker_id" parameter specifying the ID
        of the Docker image implementing the package.
        """
        docker_id = request.params.docker_id
        print 'Registering Docker container ' + docker_id + '...'

        container = ComputomeContainer(docker_id)
        container.compile_thrift()

        self.registry.register(service, docker_id)
        return code

    @delete('/services/<service_id>')
    def unregister(self, service):
        self.registry.unregister(service)

    @get('/services/invoke/<image>/<service_name>')
    def invoke(self, service, request):
        client = ThriftClient(service)
        response = client.send(service, request)
        return response

    def run(self):
        """
        Starts up the HTTP server on port 80.
        """
        bottle.run(host='localhost', port=80, debug=True)