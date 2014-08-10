# Public-facing HTTP REST server. Allows service discovery and invocation.

from bottle import route, run, template

@route('/hello')
def index():
    return index_named('World')

@route('/hello/<name>')
def index_named(name):
    return template('<b>Hello {{name}}</b>!\n', name=name)

run(host='localhost', port=8080, debug=True)
