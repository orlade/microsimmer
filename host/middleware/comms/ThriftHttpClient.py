from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

class ThriftHttpClient:
    """
    Connects with a Thrift server over a simple HTTP connection.
    """
    def __init__(self, service_class):
        self.service_class = service_class

        # Make socket
        transport = TSocket.TSocket('localhost', 9090)
        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)
        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # Create a client to use the protocol encoder
        self.client = service_class.Client(protocol)
        # Connect!
        transport.open()

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
            return method()
        else:
            print_args = map(lambda s: (str(s)[:72] + '...') if len(str(s)) > 75 else s, arguments)
            print(' >> Calling Thrift service method "%s" with arguments %s' % (method_name, print_args))
            return method(*arguments)