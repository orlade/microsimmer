# Utility functions to assist the service handler.

SECONDS_IN_HOUR = 60 * 60

EXTENSIONS = {
    'network': '.net.xml',
    'trips': '.trips.xml',
    'routes': '.rou.xml',
    'config': '.sumo.cfg',
    'additional': '.add.xml',
    'output': '.out.xml',
}


def convert_osm_to_sumo(osm_network):
    # TODO(orlade): Implement conversion via netconvert.
    network = ''
    return network


def generate_random_routes():
    # TODO(orlade): Implement route generation.
    # sumoHome + "/tools/trip/randomTrips.py")
    # python " + randomTripsPath + " -e " + SECONDS_IN_DAY + " -n " + networkPath + " -o " + outPath + " -r " + routesPath;
    routes = ''
    return routes


def generate_output_spec(output_file_path):
    # Generates the XML for an additional file to request output.
    return '<edgeData id="traffic" file="%s" freq="%d"/>' % (output_file_path, SECONDS_IN_HOUR)


def build_data_filename(job, filetype):
    return '/data/%s%s' % (job, EXTENSIONS[filetype])

def write_to_file(filename, content):
    # Writes the given content to the given file.
    f = open(filename, 'w')
    f.write(content)
    f.close()
    return filename


def read_file(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content
