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

    def invoke(self, package, service, arguments):
        """
        Invokes a method of a previously-registered service class.

        :param package: The name of the service containing the desired method.
        :param service: The name of the method to invoke.
        :param arguments: The JSON string body of the request specifying the method arguments.
        :return: The result of the invocation.
        """
        # Load the service class to get the Client class from.
        image = self.client_mediator.registry.get_service_image(package)
        return self.client_mediator.handle_invocation(image, package, service, arguments)

    def bind(self):
        """
        Starts up the HTTP server on port 5000.
        """
        @get('/')
        def home():
            packages = self.client_mediator.registry.get_registered_packages()
            return template('home.tpl', packages=packages)

        @get('/packages/<package>')
        def package_detail(package):
            services = self.client_mediator.get_services(package)
            return template('packages/detail.tpl', package=package, services=services)

        # TODO(orlade): Replace with decorators on RestServer methods.
        @post('/packages/register')
        def register():
            docker_id = request.params.docker_id
            package = request.params.package
            self.register_package(docker_id, package)
            redirect('/')

        @get('/packages/<package>/<service>')
        def service_detail(package, service):
            params = self.client_mediator.get_services(package)[service]
            return template('services/detail.tpl', package=package, service=service, params=params)

        # TODO(orlade): Proper namespacing for services.
        @post('/packages/<package>/<service>/invoke')
        def invoke(package, service):
            # Prepare the arguments to invoke the method with.
            params = self.client_mediator.get_services(package)[service]
            args = [request.params[p] for p in params]
            return self.invoke(package, service, args)

        @get('/packages/<package>/unregister')
        def confirm_unregister(package):
            return template('packages/unregister.tpl', package=package)

        @post('/packages/<package>/unregister')
        def unregister(package):
            self.unregister_package(package)
            redirect('/')

        return self

    def run(self):
        bottle.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
