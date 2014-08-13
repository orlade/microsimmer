from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from host.server.transport.TAmqpClient import TAmqpClient
from unit_tests.util import AMQP_PARAMS, TEST_EXCHANGE, TEST_REQUEST_QUEUE, TEST_RESULT_QUEUE


class ThriftServer:
    pass


class ThriftClient:
    def __init__(self, service_class):
        self.service_class = service_class

        # Create transports.
        self.__treq = TAmqpClient(AMQP_PARAMS, TEST_EXCHANGE, TEST_REQUEST_QUEUE)
        self.__tres = TAmqpClient(AMQP_PARAMS, TEST_EXCHANGE, TEST_RESULT_QUEUE)
        # Create protocols.
        req_prot = TBinaryProtocol(self.__treq)
        res_prot = TBinaryProtocol(self.__tres)

        self.client = service_class.Client(req_prot, res_prot)

        # product = client.multiply(4, 5)
        # print '4*5=%d' % (product)  # Close!
        # transport.close()

    # TODO(orlade): Allow map of keyword arguments instead, parse from JSON.
    def send(self, method, arguments):
        """
        Uses the client to invoke the target method with the given arguments.

        :param method: The method of the client to invoke.
        :param arguments: The arguments (positional list) to pass to the client method.
        :return: The response from the client.
        """
        return self.client[method](*arguments)