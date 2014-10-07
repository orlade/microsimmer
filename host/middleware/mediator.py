"""
Converts requests from the server into client calls.
"""
from distutils import dir_util
import shutil
import os

from host.middleware.registry import Registry
from host.middleware.comms.ThriftHttpClient import ThriftHttpClient
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
        # TODO(orlade): Make the results of this generation more well-known.
        package_dir = container.compile_thrift()

        # TODO(orlade): Organise the contents of the package better.
        loader = ServiceLoader(self.reg_root)
        service_classes = loader.load_package(package)

        # TODO(orlade): Register service classes in a more persistent, reusable way.
        self.registry.register_dict(service_classes, package_dir)
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
        package_dir = self.registry.get_package_dir(service)

        # Invoke the worker in the container to process the request message once it's sent.
        worker_dir = self.create_worker_dir(package_dir)
        self.run_worker(image, worker_dir)

        # Build a wrapper for the invocation.
        client = ThriftHttpClient(service_class)
        # Send the invocation to the queue.
        # Note: This will block until it receives a response.
        print('Sending request message: %s' % body)
        result = client.send(method, body)
        print('Received response message: %s' % result)

        return result

    def create_worker_dir(self, package_dir):
        """
        Creates a directory containing both the generated Thrift files and the implant files (including amqplib).
        :return: The path of the created directory.
        """
        mount_dir = os.path.join(package_dir, 'mount')
        if not os.path.isdir(mount_dir):
            os.makedirs(mount_dir)

        # Copy all of the implant files.
        # TODO(orlade): Make environment variables.
        implant_dir = '/home/oliver/dev/computome/host/implant'
        thrift_dir = '/usr/local/lib/python2.7/dist-packages/thrift'
        amqplib_dir = '/usr/local/lib/python2.7/dist-packages/amqplib'
        amqplib_thrift_dir = '/usr/local/lib/python2.7/dist-packages/amqplib_thrift'
        # Copy the gen-py files.
        gen_dir = os.path.join(package_dir)

        for lib_dir in [implant_dir, thrift_dir, amqplib_dir, amqplib_thrift_dir, gen_dir]:
            dir_util.copy_tree(lib_dir, mount_dir, update=1)

        # Copy the ServiceLoader module to load the service in the container.
        models_path = os.path.join(implant_dir, '..', 'system', 'models.py')
        shutil.copyfile(models_path, os.path.join(mount_dir, 'models.py'))

        return mount_dir

    def run_worker(self, image, package_dir):
        """
        Invokes the worker in the container to pull and process the request message.
        :param image:
        :return:
        """
        container = ComputomeContainer(image)
        mount_dir = '/mnt/computome'
        mount = '%s:%s:ro' % (package_dir, mount_dir)

        # Run the worker process.
        print(' >> Starting remote worker in image %s...' % image)
        container.run('python %s/work.py' % mount_dir, volume_arg=mount, links=['mq'], async=True)