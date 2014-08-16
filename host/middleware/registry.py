class Registry:
    def __init__(self):
        self.__services = {}

    def register(self, service, service_class):
        self.__services[service] = service_class

    def register_dict(self, service_classes):
        """
        Adds all of the {service: module} map entries to the registry.
        """
        for service in service_classes:
            self.register(service, service_classes[service])

    def unregister(self, service):
        del self.__services[service]

    def get(self, service):
        return self.__services[service]