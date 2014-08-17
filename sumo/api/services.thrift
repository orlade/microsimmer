/**
 * The API for the SUMO model.
 */

/** The contents of an XML file as a string. */
typedef string xml

service SumoService {

  /**
   * Invokes SUMO from the command line.
   */
  xml call(
    /** The command line arguments. */
    1:map<string, string> clargs
  )

  /**
   * Simulates traffic for a day with random trips on the given network, with hourly output.
   */
  xml randomDayHourly(
    /** The contents of the .net.xml file. */
    1:xml network
  )

  /**
   * Simulates traffic for a day with random trips on the given OSM network, with hourly output.
   */
  xml randomDayHourlyOsm(
    /** The contents of the .osm file. */
    1:xml osm_network
  )

}
