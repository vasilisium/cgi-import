from os import listdir
from os.path import isfile, join

from xml.etree import ElementTree as ET
from xml.dom import minidom

directoryPath = '.\\xml'
resultFileName = 'result.xml'

root = ET.Element('Records')

files = [join(directoryPath, f) for f in listdir(directoryPath) if isfile(join(directoryPath, f))]
for f in files:
  # print(f)
  file =  open(f, 'r', encoding="utf-8-sig")
  xml = ET.parse(file).getroot()
  for c in xml:
    root.append(c)


ET.register_namespace("", "http://www.datapump.cig.com")
ET.ElementTree(root).write(open(resultFileName, 'wb'), encoding='utf-8')