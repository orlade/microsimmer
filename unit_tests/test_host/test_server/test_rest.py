import subprocess

from mock import Mock, MagicMock, PropertyMock

from host.server.rest import *
from host.middleware.registry import Registry
from unit_tests.test_host.test_system.test_models import TEST_PACKAGE_DIR


bottle.run = Mock()


class TestRest:
    def __init__(self):
        self.registry = MagicMock(Registry)
        self.rest = None

    def setup(self):
        self.registry.reset_mock()
        self.rest = RestServer(self.registry, reg_root=TEST_PACKAGE_DIR)

    def test_register_package(self):
        # The parameters to mock in the request.
        class MockParams:
            def __init__(self):
                self.docker_id = 'scratch'
                self.package = 'scratch'
                self.service = 'scratch'

        type(bottle.request).params = PropertyMock(return_value=MockParams())
        subprocess.call = Mock()
        ServiceLoader.load_service = Mock(return_value={})

        self.rest.register_package()

        subprocess.call.assert_called_once()
        ServiceLoader.load_service.assert_called_once()


    def test_unregister(self):
        package = 'Foo'
        self.rest.unregister_package(package)


    def test_invoke(self):
        service = 'Foo'
        request = '{"a": 1}'
        self.rest.invoke(service, request)


    def test_run(self):
        self.rest.run()
        bottle.run.assert_called_once()