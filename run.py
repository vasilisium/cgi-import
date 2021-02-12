from my_watchdog import WatchDog, EventHandler_WithLog
from utils import validate, zip1, getXmlValues, toBase64, formatXML, writeXml, getFileName, getFileBaseName
from my_request import post

import os

def processXML(file):
  validation_result = validate(file, './SRC_Contract_UAv1.xsd')
  if validation_result:
    zip1(file)
  return validation_result

def processZip(file):
  # res = send_zip(file)

  zip_data = toBase64(file)
  res = post(zip_data)
  xml = formatXML(res[1])

  filename = getFileBaseName(getFileName(file))
  filename = os.path.splitext(filename)[0]

  writeXml(filename, xml)

  xml_msg = getXmlValues(res[1])
  return f'\n\t\tHTTP STATUS {res[0]}\n{xml_msg}'

if __name__ == "__main__":
  handlers = {
    './xml': EventHandler_WithLog('*.xml', processXML),
    './zip': EventHandler_WithLog('*.zip', processZip),
  }
  WatchDog(handlers).start()