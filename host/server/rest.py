import bottle
from bottle import route, request

from host.server.comm import ThriftClient
from host.server.registry import Registry
from host.system.constants import PACKAGE_ROOT
from host.system.docker import ComputomeContainer
from host.system.models import ServiceLoader


def methodroute(route, method='GET'):
    def decorator(f):
        print 'deco', f
        f.route = route
        return f

    return decorator


class RestServer:
    def __init__(self, registry=None, reg_root=PACKAGE_ROOT):
        if registry is None:
            registry = Registry()
        self.registry = registry
        self.reg_root = reg_root

    @methodroute('/services/register', method='POST')
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


    @methodroute('/services/<service_id>', method='DELETE')
    def unregister_package(self, service):
        self.registry.unregister(service)


    @methodroute('/services/invoke/<image>/<service_name>')
    def invoke(self, service, request):
        ServiceClass = self.registry.get(service)
        client = ThriftClient(ServiceClass)
        response = client.send(service, request)
        return response


    def run(self):
        """
        Starts up the HTTP server on port 80.
        """
        bottle.run(host='localhost', port=80, debug=True)