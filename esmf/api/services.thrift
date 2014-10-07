/**
 * The API for the ESMF regridding example model.
 */

/** The contents of an XML file as a string. */
typedef string xml

service CoupledFlowService {

  /**
   * Invokes the CoupledFlow simulation from the command line.
   */
  xml call(
    /** The command line arguments. */
    1:map<string, string> clargs
  )

  /**
   * Simulates the coupled flow demo.
   */
  xml simulate_demo()

}
