# Invokes NetLogo models.
# See http://ccl.northwestern.edu/netlogo/docs/behaviorspace.html
import subprocess
from timeit import default_timer as timer
from uuid import uuid4

from netlogo.api.experiment import Experiment

NETLOGO_HOME = '/opt/netlogo'
COMMAND = '%s/netlogo-headless.sh' % NETLOGO_HOME


def build_clargs(clargs):
    """
    Converts a map of command-line flags and values into a string of command-line inputs.
    """
    args = [COMMAND]
    for key in clargs.keys():
        args.append(key)
        # Append non-empty values after the flag.
        if clargs[key] is not None and str(clargs[key]):
            args.append(str(clargs[key]))
    return args


class NetLogoServiceHandler(object):
    """
    Implements the NetLogoService interface.
    """

    def call(self, clargs):
        """
        Simply calls headless NetLogo with the given command-line arguments.
        """
        start = timer()
        result = subprocess.call(build_clargs(clargs))
        print 'Ran experiment in %.1f sec' % (timer() - start)
        return result

    def call_experiment(self, model, setup_file, name, out_path):
        """
        Executes the specified experiment, writing the results to out_path in table format.
        """
        self.call({
            '--model': model,
            '--setup-file': setup_file,
            '--experiment': name,
            '--table': out_path
        })

    def altruism(self, altruisticProbability, selfishProbability, altruismCost, altruismBenefit, disease, harshness,
                 numTicks):
        """
        Runs an experiment of the Biology/Evolution/Altruism model.

        :returns: The table output of the experiment.
        """
        job = uuid4()
        exp_path = '/var/computome/%s/experiment.xml' % job
        out_path = '/var/computome/%s/out.csv' % job

        params = {
            'altruistic-probability': altruisticProbability,
            'selfish-probability': selfishProbability,
            'cost-of-altruism': altruismCost,
            'benefit-from-altruism': altruismBenefit,
            'disease': disease,
            'harshness': harshness,
        }

        exp = Experiment(steps=numTicks, params=params)
        exp.add_metric(color='pink')
        exp.add_metric(color='green')
        exp.write_xml(exp_path)

        model = '%s/models/Sample Models/Biology/Evolution/Altruism.nlogo' % NETLOGO_HOME
        self.call_experiment(model, exp_path, exp.name, out_path)

        with open(out_path, 'r') as out_file:
            return out_file.read()
