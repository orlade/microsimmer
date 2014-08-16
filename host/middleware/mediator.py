"""
Converts requests from the server into client calls.
"""
from host.middleware.registry import Registry
from host.server.comm import ThriftClient
from host.system.constants import PACKAGE_ROOT
from host.system.docker import ComputomeContainer
from host.system.models import ServiceLoader


class ClientMediator(object):
    def __init__(self, registry=None, reg_root=PACKAGE_ROOT):
        if registry is None:
            registry = Registry()
        self.registry = registry

        self.reg_root = reg_root

    def handle_registration(self, docker_id, package):
        """
        Registers the given Docker container with the system.
        :param docker_id:
        :param package:
        :return:
        """
        print('Registering Docker container %s...' % docker_id)

        container = ComputomeContainer(docker_id)
        container.compile_thrift()

        # TODO(orlade): Organise the contents of the package better.
        loader = ServiceLoader(self.reg_root)
        service_classes = loader.load_package(package)

        # TODO(orlade): Register service classes in a more persistent, reusable way.
        self.registry.register_dict(service_classes)
        # TODO(orlade): Register handler methods with services.

        return service_classes

    def handle_unregistration(self, service):
        self.registry.unregister(service)

    def handle_invocation(self, image, service, body):
        """
        Sends a request to invoke the given service through a Client.
        :param image: The Docker image that the service lives in.
        :param service: The name of the service to invoke.
        :param body: The body of the request containing the arguments.
        :return: The result of the invocation.
        """
        # Load the service class to get the Client class from.
        service_class = self.registry.get(service)

        # Build a wrapper for the invocation.
        client = ThriftClient(service_class)
        # Send the invocation to the queue.
        result = client.send(service, body)

        # Invoke the worker in the container.
        container = ComputomeContainer(image)
        # TODO(orlade): Run the worker script.
        mount_dir = '_mount'
        # mount = 'implant:/%s:ro' % mount_dir
        # result = container.run('python /%s/work.py' % mount_dir, volume_arg=mount)

        return result