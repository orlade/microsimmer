from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from unit_tests.test_host.test_system.test_models import TEST_PACKAGE_DIR


class MockService:
    pass

TEST_SERVICE = 'mock'
TEST_CLASS = MockService

reg = None

def setup():
    global reg
    reg = Registry()

from host.middleware.registry import Registry

def test_register():
    reg.register(TEST_SERVICE, TEST_CLASS, TEST_PACKAGE_DIR)
    assert_that(reg.get(TEST_SERVICE), equal_to(TEST_CLASS))