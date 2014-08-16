from mock import MagicMock
from host.system.docker import Container, ComputomeContainer

import os
import subprocess
from unit_tests.test_host.test_system.test_models import TEST_PACKAGE_DIR

TEST_IMAGE = 'scratch'

original_call = subprocess.call


class TestContainer:
    def __init__(self):
        self.container = None

    def setup(self):
        subprocess.call = MagicMock(name='call')
        self.container = Container(TEST_IMAGE)

    def teardown(self):
        subprocess.call = original_call

    def test_run(self):
        self.container.run(['ls'])
        subprocess.call.assert_called_once_with(['sudo', 'docker', 'run', '-t', TEST_IMAGE, 'ls'])

    def test_run_unicode(self):
        self.container.run(u'foo')
        subprocess.call.assert_called_once_with(['sudo', 'docker', 'run', '-t', TEST_IMAGE, 'foo'])

    def test_run_volume(self):
        mount = '/opt:/data'
        self.container.run('ls', volume_arg=mount)
        subprocess.call.assert_called_once_with(['sudo', 'docker', 'run', '-t', '-v', mount, TEST_IMAGE, 'ls'])


class TestComputomeContainer:
    def __init__(self):
        self.container = None

    def setup(self):
        subprocess.call = MagicMock(name='call')
        self.container = ComputomeContainer(TEST_IMAGE)

    def teardown(self):
        subprocess.call = original_call

    def test_compile_thrift(self):
        self.container.compile_thrift(TEST_PACKAGE_DIR)

        # TODO(orlade): Fix test expectation.
        # mount = '%s:%s' % (TEST_PACKAGE_DIR, '/_output')
        # command = 'thrift --gen py -o /_output/scratch /api/services.thrift'
        # arguments = ['sudo', 'docker', 'run', '-v', mount, TEST_IMAGE]
        # arguments += command.split(' ')
        # subprocess.call.assert_called_with(arguments)