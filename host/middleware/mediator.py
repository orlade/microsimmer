"""
Converts requests from the server into client calls.
"""
from host.middleware.registry import Registry
from host.middleware.comm import ThriftClient
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

    def handle_unregistration(self, package):
        self.registry.unregister(package)

    def handle_invocation(self, image, service, method, body):
        """
        Sends a request to invoke the given service through a Client.
        :param image: The Docker image that the service lives in.
        :param service: The name of the service containing the desired method.
        :param method: The name of the method to invoke.
        :param body: The body of the request containing the arguments.
        :return: The result of the invocation.
        """
        # Load the service class to get the Client class from.
        service_class = self.registry.get(service)

        # Invoke the worker in the container to process the request message once it's sent.
        self.run_worker(image)

        # Build a wrapper for the invocation.
        client = ThriftClient(service_class)
        # Send the invocation to the queue.
        # Note: This will block until it receives a response.
        result = client.send(method, body)

        return result

    def run_worker(self, image):
        """
        Invokes the worker in the container to pull and process the request message.
        :param image:
        :return:
        """
        print('Starting remote worker in image %s...' % image)
        container = ComputomeContainer(image)
        # TODO(orlade): Run the worker script.
        implant_dir = '/home/oliver/dev/computome/host/implant'
        mount_dir = '_mount'
        mount = '%s:/%s:ro' % (implant_dir, mount_dir)
        container.run('-t python /%s/work.py' % mount_dir, volume_arg=mount)
