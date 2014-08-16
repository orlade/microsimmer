import subprocess

from mock import Mock, MagicMock, PropertyMock

from host.server.rest import *
from host.middleware.registry import Registry
from unit_tests.test_host.test_system.test_models import TEST_PACKAGE_DIR

TEST_PACKAGE = 'scratch'

bottle.run = Mock()


class TestRest:
    def __init__(self):
        self.registry = MagicMock(Registry)
        self.client_mediator = MagicMock(ClientMediator)
        self.rest = None

    def setup(self):
        self.client_mediator.reset_mock()
        self.rest = RestServer(self.client_mediator)

    def test_register_package(self):
        self.rest.register_package(TEST_PACKAGE)
        self.client_mediator.handle_registration.assert_called_once_with(TEST_PACKAGE, TEST_PACKAGE)


    def test_unregister(self):
        package = 'Foo'
        self.rest.unregister_package(package)
        self.client_mediator.handle_unregistration.assert_called_once_with(package)


    def test_invoke(self):
        service = 'Foo'
        method = 'test'
        body = {"a": 1}
        self.rest.invoke(TEST_PACKAGE, service, method, body)


    def test_run(self):
        self.rest.run()
        bottle.run.assert_called_once()