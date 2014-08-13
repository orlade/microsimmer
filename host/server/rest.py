import bottle
from bottle import get, post, delete, request

from host.server.comm import ThriftClient
from host.server.registry import Registry
from host.system.constants import PACKAGE_ROOT
from host.system.docker import ComputomeContainer, image_to_package_name
from host.system.models import ServiceLoader


class RestServer:
    def __init__(self, registry=None, reg_root=PACKAGE_ROOT):
        if registry is None:
            registry = Registry()
        self.registry = registry
        self.reg_root = reg_root

    def register_package(self):
        """
        Registers a package to a Docker image ID. The request should contain a "docker_id" parameter specifying the ID
        of the Docker image implementing the package.
        """
        docker_id = request.params.docker_id
        package = request.params.package
        if not package:
            package = image_to_package_name(docker_id)

        print 'Registering Docker container %s...' % docker_id

        container = ComputomeContainer(docker_id)
        container.compile_thrift()

        # TODO(orlade): Organise the contents of the package better.
        loader = ServiceLoader(self.reg_root)
        service_classes = loader.load_package(package)

        # TODO(orlade): Register service classes in a more persistent, reusable way.
        self.registry.register_dict(service_classes)
        # TODO(orlade): Register handler methods with services.

        return "Registered %d services in package %s" % (len(service_classes), package)

    def unregister_package(self, service):
        """
        Unregisters a service module that was previously registered.
        """
        self.registry.unregister(service)

    def invoke(self, image, service):
        """
        Invokes a method of a previously-registered service class.

        :param image: The Docker image that the service lives inside.
        :param service: The name of the service method to invoke.
        :return: The result of the invocation.
        """
        # Prepare the arguments to invoke the method with.
        body = request.json

        # Load the service class to get the Client class from.
        service_class = self.registry.get(service)

        # Build a wrapper for the invocation.
        client = ThriftClient(service_class)
        # Send the invocation to the queue.
        response = client.send(service, request)

        # Invoke the worker in the container.
        container = ComputomeContainer(image)
        # TODO(orlade): Run the worker script.
        mount_dir = '_mount'
        # mount = 'implant:/%s:ro' % mount_dir
        # container.run('python /%s/work.py' % mount_dir, volume_arg=mount)

        return response

    def run(self):
        """
        Starts up the HTTP server on port 80.
        """
        # TODO(orlade): Replace with decorators on RestServer methods.
        @post('/services/register')
        def register():
            return self.register_package()

        @delete('/services/<service_id>')
        def unregister(service):
            return self.unregister_package(service)

        # TODO(orlade): Proper namespacing for services.
        @get('/services/invoke/<image>/<service_name>')
        def invoke(image, service):
            return self.invoke(image, service)

        bottle.run(host='localhost', port=80, debug=True)
