"""
Contains classes wrapping various Docker functionality at the core of Computome.
"""

import subprocess


class Container:
    """
    API for an object mapping methods onto Docker commands.
    """

    def __init__(self, image):
        self.image = image

    @classmethod
    def _execute(cls, arguments):
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
    def compile_thrift(self, host_dir):
        pass


def generate_thrift(image_id):
    """
    Copies the Thrift IDL from the Docker image with the given ID and compiles
    it to the 
    :param image_id:
    :return:
    """
    pass