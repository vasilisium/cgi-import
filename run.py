from my_watchdog import WatchDog, EventHandler_WithLog
from utils import validate, zip, getXmlValues, toBase64, formatXML, writeXml
from my_request import post
from req import send_zip
from ntpath import basename
import os

def processXML(file):
  validation_result = validate(file, './SRC_Contract_UAv1.xsd')
  if validation_result:
    zip(file)
  return validation_result

def processZip(file):
  # res = send_zip(file)

  zip_data = toBase64(file)
  res = post(zip_data)
  xml = formatXML(res[1])

  filename = basename(file)
  filename = os.path.splitext(filename)[0]

  writeXml(filename, xml)

  xml_msg = getXmlValues(res[1])
  return f'\nHTTP STATUS {res[0]}\n{xml_msg}'

if __name__ == "__main__":
  handlers = {
    './xml': EventHandler_WithLog('*.xml', processXML),
    './zip': EventHandler_WithLog('*.zip', processZip),
  }
  WatchDog(handlers).start()