from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from host.implant.network import amqp_connect, build_req_transport


class ThriftAmqpClient:
    def __init__(self, service_class):
        self.service_class = service_class

        channel = amqp_connect()
        req_transport = build_req_transport(channel)
        req_protocol = TBinaryProtocol(req_transport)
        self.client = service_class.Client(req_protocol)

    # TODO(orlade): Allow map of keyword arguments instead, parse from JSON.
    def send(self, method_name, arguments):
        """
        Uses the client to invoke the target method with the given arguments.

        :param method_name: The name of the method of the client to invoke.
        :param arguments: The arguments (positional list) to pass to the client method.
        :return: The response from the client.
        """
        method = getattr(self.client, method_name)
        # TODO(orlade): Fix blocking breaking tests.
        if arguments is None:
            print(' >> Calling Thrift service method "%s" with no arguments' % method_name)
            method()
        else:
            print(' >> Calling Thrift service method "%s" with arguments %s' % (method_name, arguments))
            return method(*arguments)