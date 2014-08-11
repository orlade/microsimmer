import amqp

from thrift.transport.TTransport import TTransportBase


class TAmqpClient(TTransportBase):
    """
    AMQP implementation of TTransport base.
    """

    def __init__(self, params, exchange, queue):
        self.__connection = None
        self.__channel = None
        self.params = params
        self.exchange = exchange
        self.queue = queue

    def open(self):
        # Set up the connection.
        self.__connection = amqp.Connection(**self.params)
        self.__channel = self.__connection.channel()

        self.__channel.exchange_declare(exchange=self.exchange, type='direct', durable=True, auto_delete=False)

        self.__channel.queue_declare(queue=self.queue, durable=True, auto_delete=False)
        self.__channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key=self.queue)

    def close(self):
        self.__connection.close()

    def isOpen(self):
        return self.__connection is not None and self.__connection.is_alive()

    def read(self, sz=-1):
        return self.__channel.basic_get(self.queue)

    def write(self, buf):
        self.__channel.basic_publish(buf, exchange=self.exchange, routing_key=self.queue)

    def flush(self):
        pass
