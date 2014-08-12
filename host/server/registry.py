class Registry:
    def __init__(self):
        self.__services = {}

    def register(self, service, ServiceClass):
        self.__services[service] = ServiceClass

    def unregister(self, service, ServiceClass):
        self.__services[service] = ServiceClass

    def get(self, service):
        return self.__services[service]