"""
Contains classes wrapping various Docker functionality at the core of Computome.
"""

import subprocess

from host.system.constants import PACKAGE_ROOT


class Container:
    """
    API for an object mapping methods onto Docker commands.
    """

    def __init__(self, image, package=None):
        if package is None:
            package = image_to_package_name(image)

        self.image = image
        self.package = package

    @classmethod
    def _execute(cls, arguments):
        """
        Executes Docker with the given arguments.

        :param arguments: The arguments to follow "sudo docker" on the command line.
        :return: The response provided by Docker.
        """
        # TODO(orlade): Allow return of container stdout.
        return subprocess.call(['sudo', 'docker'] + arguments)

    def run(self, command, volume_arg=None):
        """
        Executes the given command in the terminal of the container.

        :param command: An array of terms of the command to run.
        :param volume_arg: A string representing the mounting of a host volume to the container. For example,
        host/dir:container/dir[:ro]
        :return: The result of the Docker invocation.
        """
        # Ensure the command is a list of instructions.
        if isinstance(command, str):
            command = command.split(' ')

        arguments = ['run', self.image] + command

        # Insert the volume mounting argument if requested.
        if volume_arg is not None:
            arguments[1:1] = ['-v', volume_arg]

        return self._execute(arguments)

    def kill(self):
        """
        Terminate the container process.
        """
        pass


class ComputomeContainer(Container):
    def compile_thrift(self, host_dir=PACKAGE_ROOT):
        """
        Executes the Docker command necessary to compile the image's Thrift specification into the given directory on
        the host machine.

        :param host_dir: The directoy on the host machine in which Thrift's generated "*-gen" directories will be
        compiled.
        """
        output_dir = '/_output'
        api_dir = '/api'
        mount = '%s:%s' % (host_dir, output_dir)
        command = 'thrift --gen py -o %s/%s %s/services.thrift' % (output_dir, self.package, api_dir)
        self.run(command, volume_arg=mount)


def image_to_package_name(image_id):
    """
    Generates a package name for a Docker image based on its ID.
    :param image_id:
    :return:
    """
    return image_id.replace('/', '_')