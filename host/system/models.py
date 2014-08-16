import os
import sys
import importlib

from host.system.constants import PACKAGE_ROOT

THRIFT_FILES = ('ttypes.py', 'constants.py', '__init__.py')


class ServiceLoader:
    def __init__(self, root=PACKAGE_ROOT):
        """
        :param root: The host directory into which all models IDLs are compiled (in their own subdirectories).
        """
        self.root = root

        # Ensure the root directory exists.
        if not os.path.isdir(self.root):
            os.makedirs(self.root)

    def list_packages(self):
        """
        :return: A list of name of compiled packages.
        """
        return filter(self.is_valid_package, [os.path.join(self.root, f) for f in os.listdir(self.root)])

    def list_services(self, packages=None):
        """
        Lists the services that have been compiled for the given packages, or for all packages if None.
        :param packages: The packages to retrieve services for.
        :return: A list of names of compiled services.
        """
        services = []
        if packages is None:
            packages = self.list_packages()

        for package in packages:
            services_dir = os.path.join(self.root, package, 'gen-py', 'services')
            if os.path.isdir(services_dir):
                services += filter(self.is_service_module, os.listdir(services_dir))

        # Strip the file extensions.
        return map(lambda f: f.strip('.py'), services)

    def load_package(self, package):
        """
        Loads the service class module specified in the requested package.

        :param package: The package containing the services.
        :return: A map of service names to loaded service modules.
        """
        service_dir = os.path.join(self.root, package, 'gen-py', 'services')
        sys.path.append(service_dir)
        print('Added %s to path, loading modules...' % service_dir)
        services = self.list_services([package])
        return {s: importlib.import_module(s) for s in services}

    @staticmethod
    def is_valid_package(package):
        num_files = len([name for name in os.listdir(package)])
        return os.path.isdir(package) and num_files > 0

    @classmethod
    def is_service_module(cls, name):
        """
        Determines whether a given Thrift-generated filename contains a service class.
        :param name: The filename to test.
        :return: True if the file contains a service class, or False otherwise.
        """
        if name in THRIFT_FILES:
            return False
        if not name.endswith('.py'):
            return False
        return True