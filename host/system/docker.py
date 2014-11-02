"""
Contains classes wrapping various Docker functionality at the core of Computome.
"""

import subprocess
import os

from host.system.constants import PACKAGE_ROOT


class Container:
    """
    API for an object mapping methods onto Docker commands.
    """

    def __init__(self, image, package=None):
        if package is None:
            package = image_to_package_name(image)
        assert package

        self.image = image
        self.package = package

    @staticmethod
    def _execute(arguments, async=False):
        """
        Executes Docker with the given arguments.

        :param arguments: A list of the arguments to follow "sudo docker" on the command line.
        :return: The response provided by Docker.
        """
        # TODO(orlade): Allow return of container stdout.
        arguments = ['sudo', 'docker'] + arguments
        print(' $$ Executing: %s [async=%s]' % (' '.join(arguments), async))
        if async:
            return subprocess.Popen(arguments)
        else:
            return subprocess.call(arguments)

    def run(self, command, volume_arg=None, ports=None, links=None, async=False, name=None):
        """
        Executes the given command in the terminal of the container.

        :param command: An array of terms of the command to run.
        :param volume_arg: A string representing the mounting of a host volume to the container. For example,
        host/dir:container/dir[:ro]
        :return: The result of the Docker invocation.
        """
        # Ensure the command is a list of instructions.
        if isinstance(command, basestring):
            command = str(command).split(' ')

        # TODO(orlade): Determine why -t is necessary.
        arguments = ['run', '-t', '--entrypoint', '/bin/sh']

        if not name is None:
            arguments += ['--name'] + [name]

        # Insert the volume mounting argument if requested.
        if volume_arg is not None:
            arguments += ['-v', volume_arg]

        if not links is None:
            arguments += ['--link'] + ['%s:%s' % (link, link) for link in links]

        if not ports is None:
            for outside, inside in ports.items():
                arguments += ['-p', '%s:%s' % (outside, inside)]

        arguments += [self.image, '-c'] + [' '.join(command)]

        return self._execute(arguments, async=async)

    def kill(self):
        """
        Terminate the container process.
        """
        pass


class ComputomeContainer(Container):
    def compile_thrift(self, host_dir=PACKAGE_ROOT):
        """
        Compiles the image's Thrift specification into the given directory on the host machine. Involves copying the API
        specification out of the container to be compiled on the host (assuming responsibility for the Thrift
        dependency).

        :param host_dir: The directory on the host machine in which Thrift's generated directories will be compiled.
        :return: The output directory for the generated Thrift code.
        """
        # The location that the model API files should be stored.
        api_dir_name = 'api'
        api_dir = '/%s' % api_dir_name

        # The location to mount to in the container.
        mount_dir = '/_mount'

        # The location to copy the API files into for compilation.
        package_dir = os.path.join(host_dir, self.package)
        if not os.path.isdir(package_dir):
            os.makedirs(package_dir)

        # The Docker mount (volume) argument.
        mount = '%s:%s' % (package_dir, mount_dir)

        # Copy the API files out.
        self.run('cp -r %s %s' % (api_dir, mount_dir), volume_arg=mount)

        # Path to the copied services.thrift IDL file.
        thrift_path = '%s/%s/services.thrift' % (package_dir, api_dir_name)
        # Compile the Thrift IDL.
        thrift_command = 'thrift --gen py -o %s %s' % (package_dir, thrift_path)
        print('Executing: %s' % thrift_command)
        subprocess.call(thrift_command.split(' '))
        return package_dir


def image_to_package_name(image_id):
    """
    Generates a package name for a Docker image based on its ID.
    :param image_id:
    :return:
    """
    return image_id.replace('/', '_')

def stop_container(name):
    """
    Calls `docker stop` on the container with the given name.
    """
    Container._execute(['stop', '-t', '1', name], async=True)
