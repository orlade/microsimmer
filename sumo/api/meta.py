# Information about the service.

def get_id():
  return 'sumo'

# The Docker image with SUMO installed.
def get_image():
  return 'pie21/sumo-manual'

def command():
  return 'sumo'
