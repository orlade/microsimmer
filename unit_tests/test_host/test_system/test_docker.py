from mock import MagicMock
from host.system.docker import Container, ComputomeContainer

import os
import subprocess
from unit_tests.test_host.test_system.test_models import TEST_PACKAGE_DIR

TEST_IMAGE = 'scratch'


class TestContainer:
    def __init__(self):
        self.container = None

    def setup(self):
        subprocess.call = MagicMock(name='call')
        self.container = Container(TEST_IMAGE)

    def teardown(self):
        subprocess.call.reset_mock()

    def test_run(self):
        self.container.run(['ls'])
        subprocess.call.assert_called_once_with(['sudo', 'docker', 'run', TEST_IMAGE, 'ls'])

    def test_run_volume(self):
        mount = '/opt:/data'
        self.container.run('ls', volume_arg=mount)
        subprocess.call.assert_called_once_with(['sudo', 'docker', 'run', '-v', mount, TEST_IMAGE, 'ls'])


class TestComputomeContainer:
    def __init__(self):
        self.container = None

    def setup(self):
        subprocess.call = MagicMock(name='call')
        self.container = ComputomeContainer(TEST_IMAGE)

    def teardown(self):
        subprocess.call.reset_mock()

    def test_compile_thrift(self):
        self.container.compile_thrift(TEST_PACKAGE_DIR)

        mount = '%s:%s' % (TEST_PACKAGE_DIR, '/_output')
        command = 'thrift --gen py -o /_output/scratch /api/services.thrift'
        arguments = ['sudo', 'docker', 'run', '-v', mount, TEST_IMAGE]
        arguments += command.split(' ')
        subprocess.call.assert_called_once_with(arguments)