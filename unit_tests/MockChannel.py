from amqp.channel import Channel
from mock import Mock, PropertyMock, MagicMock
from unit_tests.util import TEST_EXCHANGE

__queue = []
__is_open = False

mock_channel = None


def add_message(msg, exchange=TEST_EXCHANGE, routing_key='req'):
    __queue.append(msg)


def get_message(queue=''):
    return __queue.pop(0)


def mock_open():
    type(mock_channel).is_open = PropertyMock(return_value=True)
    # global __is_open
    # __is_open = True


def mock_close():
    type(mock_channel).is_open = PropertyMock(return_value=False)
    # global __is_open
    # __is_open = False


def build_mock_channel():
    mock_channel = MagicMock(Channel)
    mock_channel.basic_publish = Mock(side_effect=add_message)
    mock_channel.basic_get = Mock(side_effect=get_message)
    type(mock_channel).is_open = PropertyMock(return_value=False)
    mock_channel.open = Mock(side_effect=mock_open)
    mock_channel.close = Mock(side_effect=mock_close)
    return mock_channel


def populate(messages=None):
    global __queue
    if messages is None:
        messages = []
    __queue = messages