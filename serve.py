#!/usr/bin/python
import bottle

from host.server.rest import RestServer

server = RestServer().bind()

if __name__ == '__main__':
    server.run()

# Register standard WSGI app for gunicorn.
app = bottle.default_app()