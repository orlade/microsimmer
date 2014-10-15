import os

from host.system.constants import PACKAGE_ROOT


class Registry:
    def __init__(self):
        self.__services = {}
        self.__service_images = {}
        self.__service_dirs = {}

    def register(self, image, service, service_class, package_dir=None):
        if package_dir is None:
            package_dir = os.path.join(PACKAGE_ROOT, service_class)
        self.__services[service] = service_class
        self.__service_images[service] = image
        self.__service_dirs[service] = package_dir

    def register_dict(self, image, service_classes, package_dir=None):
        """
        Adds all of the {service: module} map entries to the registry.

        :param service_classes: A map of service names to modules.
        :param package_dir: The directory into which the services were compiled.
        """
        for service in service_classes:
            self.register(image, service, service_classes[service], package_dir)

    def unregister(self, service):
        del self.__services[service]

    def get(self, service):
        return self.__services[service]

    def get_package_dir(self, service):
        return self.__service_dirs[service]

    def get_service_image(self, service):
        return self.__service_images[service]

    def get_registered_packages(self):
        return self.__services.keys()