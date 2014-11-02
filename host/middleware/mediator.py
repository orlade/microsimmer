"""
Converts requests from the server into client calls.
"""
from distutils import dir_util
import shutil
import os
from uuid import uuid4
from host.middleware.inspector import get_thrift_methods

from host.middleware.registry import Registry
from host.middleware.comms.ThriftHttpClient import ThriftHttpClient
from host.system.constants import PACKAGE_ROOT
from host.system.docker import ComputomeContainer, stop_container
from host.system.models import ServiceLoader

PYTHON_PACKAGE_PATH = '/usr/local/lib/python2.7/dist-packages'
COMPUTOME_HOME = '/opt/computome'


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
        self.registry.register_dict(docker_id, service_classes, package_dir)
        # TODO(orlade): Register handler methods with services.

        return service_classes

    def handle_unregistration(self, package):
        self.registry.unregister(self.registry.get(package))

    def get_services(self, package):
        """Returns a list of services available in the named package."""
        return get_thrift_methods(self.registry.get(package))

    def handle_invocation(self, image, package, service, arguments):
        """
        Sends a request to invoke the given service through a Client.
        :param image: The Docker image that the service lives in.
        :param package: The name of the service containing the desired method.
        :param service: The name of the method to invoke.
        :param arguments: The body of the request containing the arguments.
        :return: The result of the invocation.
        """
        # Load the service class to get the Client class from.
        service_class = self.registry.get(package)
        package_dir = self.registry.get_package_dir(package)

        # Invoke the worker in the container to process the request message once it's sent.
        worker_dir = self.create_worker_dir(package_dir)
        worker_name = self.run_worker(image, package, worker_dir)
        # TODO(orlade): Retrieve assigned port and pass into Client.

        import time

        time.sleep(1)

        # Build a wrapper for the invocation.
        client = ThriftHttpClient(service_class)
        # Send the invocation to the queue.
        # Note: This will block until it receives a response.
        truncate = lambda s: (str(s)[:72] + '...') if len(str(s)) > 75 else s
        print_args = map(truncate, arguments)
        print('Sending request message: %s' % print_args)

        try:
            result = client.send(service, arguments)
            print('Received response message: %s' % truncate(result))
        finally:
            stop_container(worker_name)

        return result

    def create_worker_dir(self, package_dir):
        """
        Creates a directory containing both the generated Thrift files and the
        implant files (including amqplib).
        :return: The path of the created directory.
        """
        mount_dir = os.path.join(package_dir, 'mount')

        # Copy all of the implant files.
        # TODO(orlade): Make environment variables.
        copy_dirs = {
            '': '%s/host/implant' % COMPUTOME_HOME,
            'thrift': '%s/thrift' % PYTHON_PACKAGE_PATH,
            'gen-py': os.path.join(package_dir, 'gen-py'),
            # 'amqplib': '%s/amqplib' % PYTHON_PACKAGE_PATH,
            # 'amqplib_thrift': '%s/amqplib_thrift' % PYTHON_PACKAGE_PATH,
        }

        for key, path in copy_dirs.items():
            dir_util.copy_tree(path, os.path.join(mount_dir, key), update=1)

        # Copy the ServiceLoader module to load the service in the container.
        models_path = os.path.join(COMPUTOME_HOME, 'host', 'system', 'models.py')
        shutil.copyfile(models_path, os.path.join(mount_dir, 'models.py'))

        return mount_dir

    def run_worker(self, image, package, package_dir):
        """
        Invokes the worker in the container to pull and process the request message.
        :param image:
        :return:
        """
        container = ComputomeContainer(image)
        mount_dir = '/mnt/computome'
        mount = '%s:%s:ro' % (package_dir, mount_dir)
        ports = {9090: 9090}

        # Run the worker process.
        print(' >> Starting remote worker in image %s...' % image)
        # links=['mq']
        name = str(uuid4())
        container.run('python %s/work.py %s' % (mount_dir, package), volume_arg=mount, ports=ports, async=True,
                      name=name)
        return name