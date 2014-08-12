from mock import MagicMock
from host.system.docker import Container

import subprocess

TEST_IMAGE = 'scratch'

class TestDocker:

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