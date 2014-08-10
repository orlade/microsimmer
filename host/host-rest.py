# Public-facing HTTP REST server. Allows service discovery and invocation.

import subprocess

from bottle import post, request, route, run, template

@route('/hello')
def index():
    return index_named('World')

@route('/hello/<name>')
def index_named(name):
    return template('<b>Hello {{name}}</b>!\n', name=name)
    
@post('/services/register')
def register_service():
  image = request.params.image
  print 'Registering Docker container ' + image + '...'
  code = subprocess.call(['sudo', 'docker', 'run', image, '/bin/echo', '"Hello World"'])
  return code
  
@get('/services/invoke/<image>/<service_name>')
def invoke_service():
  print 'Invoking Docker container ' + image + '...'
  code = subprocess.call(['sudo', 'docker', 'run', image, '/bin/echo', '"Hello World"'])
  return code

# Start the server.
run(host='localhost', port=8080, debug=True)
