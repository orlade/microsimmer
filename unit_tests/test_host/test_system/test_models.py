import os

from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to

from host.system.models import ServiceLoader

TEST_DIR = os.path.abspath('/tmp')
TEST_PACKAGE_NAMES = ('a', 'b', 'c')
TEST_PACKAGES = map(lambda f: os.path.join(TEST_DIR, f), TEST_PACKAGE_NAMES)


def touch(fname):
    with open(fname, 'a'):
        os.utime(fname, (1, 1))


def setup_test_dirs():
    if not os.path.isdir(TEST_DIR):
        os.makedirs(TEST_DIR)
    for package in TEST_PACKAGES:
        if not os.path.isdir(package):
            os.makedirs(package)
        src_dir = os.path.join(package, 'gen-py', 'services')

        if not os.path.isdir(src_dir):
            os.makedirs(src_dir)
        touch(os.path.join(src_dir, package[-1].upper() + 'Service.py'))


class TestServiceLoader:
    def __init__(self):
        self.loader = None
        setup_test_dirs()

    def setup(self):
        self.loader = ServiceLoader(TEST_DIR)

    def test_list_packages(self):
        packages = self.loader.list_packages()
        assert_that(packages, equal_to(TEST_PACKAGES))

    def test_list_services(self):
        services = self.loader.list_services()
        expected = [p.upper() + 'Service' for p in TEST_PACKAGE_NAMES]
        assert_that(services, equal_to(expected))

    def test_load_service(self):
        module = self.loader.load_service('a', 'AService')
        assert_that(module is not None)


# Classmethod tests

def test_is_service_module():
    assert_that(ServiceLoader.is_service_module('FooService.py'))
    assert_that(ServiceLoader.is_service_module('Foo.py'))
    assert_that(ServiceLoader.is_service_module('Service.py'))

    assert_that(not ServiceLoader.is_service_module(''))
    assert_that(not ServiceLoader.is_service_module('__init__.py'))
    assert_that(not ServiceLoader.is_service_module('ttypes.py'))
    assert_that(not ServiceLoader.is_service_module('constants.py'))
    assert_that(not ServiceLoader.is_service_module('FooService'))
    assert_that(not ServiceLoader.is_service_module('FooService-remote'))