import os
import sys
from util import write_to_file, build_data_filename, generate_random_routes, generate_output_spec, \
    SECONDS_IN_HOUR, read_file, convert_osm_to_sumo

import subprocess
import uuid

command = 'sumo'

TRUNC_LEN = 300


def build_clargs(clargs):
    """
    Converts a map of command-line flags and values into a string of command-line inputs.
    """
    args = [command]
    for key in clargs.keys():
        args.append(key)
        # Append non-empty values after the flag.
        if clargs[key] is not None and str(clargs[key]):
            args.append(str(clargs[key]))
    return args


class SumoServiceHandler():
    """
    Implements the SumoService interface.
    """

    def call(self, clargs):
        """
        Invokes SUMO from the command line.

        Parameters:
         - clargs: The command line arguments.
        """
        job = uuid.uuid4()

        if '--net-file' in clargs and '--additional-files' not in clargs:
            output_file_path = build_data_filename(job, 'output')
            adtl_file_path = build_data_filename(job, 'additional')
            write_to_file(adtl_file_path, generate_output_spec(output_file_path))
            clargs['--additional-files'] = adtl_file_path
        else:
            # TODO(orlade): Handle cases where output file is specified.
            output_file_path = None

        args = build_clargs(clargs)

        print('Calling SUMO with arguments:\n%s' % ' '.join(args))
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)

        # Save the command-line output.
        output = {'cli': proc.stdout.read()}

        # If there was any output to a file, include that too.
        if output_file_path and os.path.isfile(output_file_path):
            with open(output_file_path) as f:
                output['data'] = f.read()

        # DEBUG: Print the results.
        truncate = lambda s: (s[:TRUNC_LEN-3] + '...') if len(s) > TRUNC_LEN else s
        print ('Output was:')
        for key in output:
            print '%s: %s' % (key, truncate(output[key]))

        return str(output)

    def randomDayHourly(self, network):
        """
        Simulates traffic for a day with random trips on the given network, with hourly output.

        Parameters:
         - network: The contents of the .net.xml file.
        """
        job = uuid.uuid4()

        net_file_path = build_data_filename(job, 'network')
        route_file_path = build_data_filename(job, 'routes')
        adtl_file_path = build_data_filename(job, 'additional')
        output_file_path = build_data_filename(job, 'output')

        write_to_file(net_file_path, network)
        if not os.path.isfile(route_file_path):
            generate_random_routes(job)
        write_to_file(adtl_file_path, generate_output_spec(output_file_path))

        args = {
            '--net-file': net_file_path,  # Network input file.
            '--route-files': route_file_path,  # Route input file.
            '--additional-files': adtl_file_path,  # Additional file specifying output format.
            '--begin': 0,  # Time to begin the simulation.
            '--end': SECONDS_IN_HOUR,  # Time to end the simulation.
            '--time-to-teleport': -1,  # Disable teleportation for vehicles that get stuck.
            '-W': None,  # Disable warning messages.
        }

        return_code = self.call(args)
        if return_code != 0:
            # TODO(orlade): Throw exceptions.
            return return_code

        return read_file(output_file_path)

    def randomDayHourlyOsm(self, osm_network):
        """
        Simulates traffic for a day with random trips on the given OSM network, with hourly output.

        Parameters:
         - osm_network: The contents of the .osm file.
        """
        return self.randomDayHourly(convert_osm_to_sumo(osm_network))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        handler = SumoServiceHandler()
        method = getattr(handler, sys.argv[1])
        print 'Calling %s %s...' % (sys.argv[1], sys.argv[2:])
        print method(handler, *sys.argv[2:])
