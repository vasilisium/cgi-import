import os
import base64
from ntpath import basename
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

import xmlschema
from lxml import etree

import config
log = config.logger

def validate(xmlFile, schemaFile):
  fileNmae = basename(xmlFile)

  schema = xmlschema.XMLSchema(schemaFile)
  result = schema.is_valid(xmlFile)
  if not result: 
    log.info('%s Invalid', fileNmae)
  return result

def zip(file):
  filename = basename(file)
  filename = os.path.splitext(filename)[0]
  archive = ZipFile(f'./zip/{filename}.zip', 'w', ZIP_DEFLATED)
  archive.write(file)
  archive.close()

def zip1(file):
  import subprocess
  zipper = subprocess.run(os.path.join('C:\\Program Files\\7-Zip\\',"7z.exe"),f'a  mx0 ')


def toBase64(filePath):
  f = open(filePath, 'rb')
  f_bytes = base64.b64encode(f.read()).decode('utf8')
  return f_bytes

def removeCredentials(data):
  # TODO: removeCredentials from output xml file
  return data

def writeXml(fileName, data):
  dt = datetime.now().strftime('%Y-%m-%d#%H-%M-%S-%f')[:-3]
  new_filePath = f'./responses/{fileName}#{dt}.xml'
  if not os.path.exists(os.path.dirname(new_filePath)):
    os.makedirs(os.path.dirname(new_filePath))
  
  with open(new_filePath, 'w') as xml:
    new_data = removeCredentials(data)
    xml.write(new_data)

  return new_filePath

def getXmlValues(xmlText):
  # xml = open(file, 'r').read()
  xml = bytes(bytearray(xmlText, encoding='utf-8'))
  xml = etree.XML(xml)

  msg = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch/Message/Description').text
  msg_TypeName = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch/Message').attrib['TypeName']

  ba_id = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch').attrib['Id']
  ba_statId = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch').attrib['StatusId']
  ba_statName = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch').attrib['StatusName']
  return f'{msg_TypeName}: {msg}\nBatch: id {ba_id} status {ba_statId}\n{ba_statName}'
  
def formatXML(xmlText):
  import xml.dom.minidom
  xml = xml.dom.minidom.parseString(xmlText)
  return xml.toprettyxml()

if __name__ == '__main__':
  zip1('./xml/5_3581801921_1.xml')