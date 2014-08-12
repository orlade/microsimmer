class Registry:
    def __init__(self):
        self.__services = {}

    def register(self, service, service_class):
        self.__services[service] = service_class

    def unregister(self, service, service_class):
        del self.__services[service]

    def get(self, service):
        return self.__services[service]