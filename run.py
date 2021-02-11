from my_watchdog import WatchDog, EventHandler_WithLog
from utils import validate, zip, to_bytes, getXmlValues

from req import send_zip

def processXML(file):
  validation_result = validate(file, './SRC_Contract_UAv1.xsd')
  if validation_result:
    zip(file)
  return validation_result

def processZip(file):
  res = send_zip(file)
  xml_msg = getXmlValues(res[1])
  return f'\nHTTP STATUS {res[0]}\n{xml_msg}'

if __name__ == "__main__":
  handlers = {
    './xml': EventHandler_WithLog('*.xml', processXML),
    './zip': EventHandler_WithLog('*.zip', processZip),
  }
  WatchDog(handlers).start()