import bottle
from bottle import get, post, delete, request

from host.server.comm import ThriftClient
from host.server.registry import Registry
from host.system.constants import PACKAGE_ROOT
from host.system.docker import ComputomeContainer
from host.system.models import ServiceLoader

__server = None


class RestServer:
    def __init__(self, registry=None, reg_root=PACKAGE_ROOT):
        if registry is None:
            registry = Registry()
        self.registry = registry
        self.reg_root = reg_root
        global __server
        __server = self

    def register_package(self):
        """
        Registers a package to a Docker image ID. The request should contain a "docker_id" parameter specifying the ID
        of the Docker image implementing the package.
        """
        docker_id = request.params.docker_id
        package = request.params.package
        service = request.params.service
        print 'Registering Docker container %s...' % docker_id

        container = ComputomeContainer(docker_id)
        container.compile_thrift()

        loader = ServiceLoader(self.reg_root)
        service_class = loader.load_service(package, service)

        return self.registry.register(service, service_class)


    def unregister_package(self, service):
        self.registry.unregister(service)


    def invoke(self, service, request):
        ServiceClass = self.registry.get(service)
        client = ThriftClient(ServiceClass)
        response = client.send(service, request)
        return response


    def run(self):
        """
        Starts up the HTTP server on port 80.
        """
        # TODO(orlade): Replace with decorators on RestServer methods.
        @post('/services/register')
        def register():
            self.register_package()

        @delete('/services/<service_id>')
        def unregister(service):
            self.unregister_package(service)

        @get('/services/invoke/<image>/<service_name>')
        def invoke(image, service):
            self.invoke(image, service)

        bottle.run(host='localhost', port=80, debug=True)
