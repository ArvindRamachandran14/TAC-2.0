import dicttoxml

import xml.etree.ElementTree as ET

from datetime import datetime

SC_T1 = (20.6, datetime.now())

SC_T2 = (10.6, datetime.now())

parmDict = {'SC_T1' : SC_T1, 'SC_T2' : SC_T2}

xmlstring = dicttoxml.dicttoxml(parmDict)

print(type(xmlstring))

root = ET.fromstring(xmlstring)

#print(root.find('SC_T1')[0].text)
