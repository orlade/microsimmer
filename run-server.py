#!/usr/bin/python

from host.server.rest import RestServer

if __name__ == '__main__':
    server = RestServer().run()