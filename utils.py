import os
import base64
from ntpath import basename
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
import xmlschema
from lxml import etree

import config
log = config.logger

def getFileName(filePath):
  return basename(filePath)

def getFileBaseName(fileName):
  return os.path.splitext(fileName)[0]

def validate(xmlFile, schemaFile):
  fileNmae = basename(xmlFile)

  schema = xmlschema.XMLSchema(schemaFile)
  result = schema.is_valid(xmlFile)
  if not result: 
    log.info('%s\t\tInvalid', fileNmae)
  return result

def zip(file):
  filename = basename(file)
  filename = os.path.splitext(filename)[0]
  archive = ZipFile(f'./zip/{filename}.zip', 'w', ZIP_DEFLATED)
  archive.write(file)
  archive.close()

def zip1(file):
  import subprocess
  fileName = getFileBaseName(getFileName(file))
  zipPath = f'./zip/{fileName}.zip'
  zPath = os.path.join('C:\\Program Files\\7-Zip\\',"7z.exe")
  subprocess.run(f'{zPath} a {zipPath} {file} mx0 ')
  return zipPath


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

  batch = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch')
  ba_id = batch.attrib['Id']
  ba_statId = batch.attrib['StatusId']
  ba_statName = batch.attrib['StatusName']

  msg = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch/Message')
  if msg:
    msg_TypeName = msg.attrib['TypeName']
    msg = msg.find('./Description').text

    return f'\t\t{msg_TypeName}: {msg}\n\t\tBatch: id {ba_id} status {ba_statId}\n\t\t{ba_statName}'
  return f'\t\tSuccess! Batch: id {ba_id} status {ba_statId}\n\t\t{ba_statName}'
  
  
def formatXML(xmlText):
  import xml.dom.minidom
  xml = xml.dom.minidom.parseString(xmlText)
  return xml.toprettyxml()

if __name__ == '__main__':
  f = open('.\\responses\-.xml').read()
  vals = getXmlValues(f)
  print(vals)