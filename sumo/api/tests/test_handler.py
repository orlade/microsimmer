import os
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from sumo.api.handler import build_clargs
from sumo.api.handler import SumoServiceHandler

from sumo.api.util import SECONDS_IN_HOUR


def test_build_clargs():
    clargs = {
        '--net-file': '/path/to/file',
        '--begin': 0,
        '-W': None,
    }
    args = ' '.join(build_clargs(clargs))
    assert_that(args, equal_to('sumo -W --net-file /path/to/file --begin 0'))


def test_call_sumo():
    output = SumoServiceHandler().call({})
    print output
    assert output['cli'].startswith('SUMO sumo Version ')


def test_call_sumo_data():
    """
    Invokes SUMO with pre-calculated data for the Eichstaett network.
    """
    output = SumoServiceHandler().call({
        '--net-file': os.path.abspath('../../example/eich.net.xml'),
        '--route-files': os.path.abspath('../../example/eich.rou.xml'),
        '--begin': 0,
        '--end': SECONDS_IN_HOUR,
        '--time-to-teleport': -1,
        '-W': None,
    })
    # TODO: Return written output.
    assert_that(output['data'].count('<edge'), equal_to(1177))


# def test_randomDayHourly():
# xml_path = 'C:\dev\workspace\computome\sumo\example\quickstart.net.xml'
#     with open(xml_path, 'r') as f:
#         xml = f.read()
#         output = SumoServiceHandler().randomDayHourly(xml)
#     print output
#     assert output.startswith('<')


def test_randomDayHourlyOsm():
    return