from host.server.rest import RestServer


def init():
    RestServer().run()