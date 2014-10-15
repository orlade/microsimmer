import os
import bottle
from bottle import get, post, delete, request, redirect
from host.middleware.mediator import ClientMediator

from host.system.docker import image_to_package_name

# The path to the views from the app's root directory.
VIEW_PATH = ['./host/server/views']


def template(*args, **kwargs):
    """Builds and renders a Bottle template with the lookup path set correctly."""
    kwargs['template_lookup'] = VIEW_PATH
    return bottle.template(*args, **kwargs)


class RestServer:
    def __init__(self, client_mediator=None):
        if client_mediator is None:
            client_mediator = ClientMediator()
        self.client_mediator = client_mediator

    def register_package(self, docker_id, package=None):
        """
        Registers a package to a Docker image ID. The request should contain a "docker_id" parameter specifying the ID
        of the Docker image implementing the package.
        """
        if not package:
            package = image_to_package_name(docker_id)

        service_classes = self.client_mediator.handle_registration(docker_id, package)

        return "Registered %d services in package %s" % (len(service_classes), package)

    def unregister_package(self, package):
        """
        Unregisters a service module that was previously registered.
        """
        self.client_mediator.handle_unregistration(package)

    def invoke(self, image, service, method, body):
        """
        Invokes a method of a previously-registered service class.

        :param image: The Docker image that the service lives inside.
        :param service: The name of the service containing the desired method.
        :param method: The name of the method to invoke.
        :param body: The JSON string body of the request specifying the method arguments.
        :return: The result of the invocation.
        """
        # Load the service class to get the Client class from.
        return self.client_mediator.handle_invocation(image, service, method, body)

    def run(self):
        """
        Starts up the HTTP server on port 80.
        """

        @get('/')
        def home():
            packages = self.client_mediator.registry.get_registered_packages()
            return template('home.tpl', services=packages)

        # TODO(orlade): Replace with decorators on RestServer methods.
        @post('/services/register')
        def register():
            docker_id = request.params.docker_id
            package = request.params.package
            self.register_package(docker_id, package)
            redirect('/')

        # TODO(orlade): Proper namespacing for services.
        @get('/services/invoke/<image>/<service_name>')
        def invoke(image, service):
            # Prepare the arguments to invoke the method with.
            body = request.json
            return self.invoke(image, service, body)

        @get('/services/<service>/unregister')
        def confirm_unregister(service):
            return template('services/unregister.tpl', service=service)

        @post('/services/<service>/unregister')
        def unregister(service):
            self.unregister_package(service)
            redirect('/')

        # Run
        bottle.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=True)
