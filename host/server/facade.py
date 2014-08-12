from host.server.rest import RestServer


def init():
    print('Intialising facade...')
    RestServer().run()

if __name__ == '__main__':
    init()