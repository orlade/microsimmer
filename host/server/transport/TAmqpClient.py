import amqp
from cStringIO import StringIO

from thrift.transport.TTransport import TTransportBase


class TAmqpClient(TTransportBase):
    """
    AMQP implementation of TTransport base.
    """

    def __init__(self, exchange, queue, channel=None, params=None):
        self.__wbuf = StringIO()
        self.__connection = None
        self.__channel = channel

        self.params = params
        self.exchange = exchange
        self.queue = queue

    def open(self):
        if self.__channel is None:
            # Set up the connection.
            self.__connection = amqp.Connection(**self.params)
            self.__channel = self.__connection.channel()

            self.__channel.exchange_declare(exchange=self.exchange, type='direct', durable=True, auto_delete=False)

            self.__channel.queue_declare(queue=self.queue, durable=True, auto_delete=False)
            self.__channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key='req')

    def close(self):
        if self.__connection is not None:
            self.__connection.close()

    def isOpen(self):
        return self.__channel is not None and self.__channel.is_open

    def read(self, sz=-1):
        return self.__channel.basic_get(queue=self.queue)

    def write(self, buf):
        self.__wbuf.write(buf)

    def flush(self):
        # Pull data out of buffer
        data = self.__wbuf.getvalue()
        self.__wbuf = StringIO()

        # Package data into an AMQP message.
        msg = amqp.Message(data)
        msg.properties['delivery_mode'] = 2
        self.__channel.basic_publish(msg, exchange=self.exchange, routing_key=self.queue)

        # Return the constructed message for testing.
        return msg
