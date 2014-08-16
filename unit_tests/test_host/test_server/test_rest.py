import subprocess

from mock import Mock, MagicMock, PropertyMock

from host.server.rest import *
from host.middleware.registry import Registry
from unit_tests.test_host.test_system.test_models import TEST_PACKAGE_DIR


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
        # The parameters to mock in the request.
        class MockParams:
            def __init__(self):
                self.docker_id = 'scratch'
                self.package = 'scratch'
                self.service = 'scratch'
        params = MockParams()

        type(bottle.request).params = PropertyMock(return_value=params)
        # subprocess.call = Mock()
        # ServiceLoader.load_service = Mock(return_value={})

        self.rest.register_package()

        self.client_mediator.handle_registration.assert_called_once_with(params.docker_id, params.package)
        # subprocess.call.assert_called_once()
        # ServiceLoader.load_service.assert_called_once()


    def test_unregister(self):
        package = 'Foo'
        self.rest.unregister_package(package)
        self.client_mediator.handle_unregistration.assert_called_once_with(package)


    def test_invoke(self):
        service = 'Foo'
        request = '{"a": 1}'
        self.rest.invoke(service, request)


    def test_run(self):
        self.rest.run()
        bottle.run.assert_called_once()