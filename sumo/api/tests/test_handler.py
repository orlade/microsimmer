from sumo.api.handler import SumoServiceHandler

def test_call():
    output = SumoServiceHandler().call({})
    print output
    assert output.startswith('SUMO sumo Version ')

def test_randomDayHourly():
    xml_path = 'C:\dev\workspace\computome\sumo\example\eichstaett.net.xml'
    with open(xml_path, 'r') as f:
        xml = f.read()
        output = SumoServiceHandler().randomDayHourly(xml)
    print output
    assert output.startswith('<')

def test_randomDayHourlyOsm():
    return