import sys
from sumo.api.meta import command
from sumo.api.util import write_to_file, build_data_filename, generate_random_routes, generate_output_spec, \
    SECONDS_IN_HOUR, read_file, convert_osm_to_sumo

sys.path.append('gen-py')

import subprocess
import uuid

class SumoServiceHandler():
    """
    Implements the SumoService interface.
    """

    def call(self, arguments):
        """
        Invokes SUMO from the command line.

        Parameters:
         - arguments: The command line arguments.
        """
        args = [command]
        for key in arguments.keys():
            args.append(key)
            if arguments[key] is not None:
                args.append(arguments[key])
        
        code = subprocess.call(args)
        # TODO(orlade): Return output contents.
        return code
        
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
        write_to_file(route_file_path, generate_random_routes())
        write_to_file(adtl_file_path, generate_output_spec(output_file_path))
        
        args = {
            '--net-file': net_file_path,          # Network input file.
            '--route-files': route_file_path,     # Route input file.
            '--additional-files': adtl_file_path, # Additional file specifying output format.
            '--begin': 0,                         # Time to begin the simulation.
            '--end': SECONDS_IN_HOUR,             # Time to end the simulation.
            '--time-to-teleport': -1,             # Disable teleportation for vehicles that get stuck.
            '-W': None,                           # Disable warning messages.
        }
        if self.call(args) != 0:
            # TODO(orlade): Throw exceptions.
            return False
        
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
