import os
import base64
from ntpath import basename
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
    log.error('%s Invalid', fileNmae)
  return result

def zip(file):
  filename = basename(file)
  filename = os.path.splitext(filename)[0]
  archive = ZipFile(f'./zip/{filename}.zip', 'w', ZIP_DEFLATED)
  archive.write(file)
  archive.close()

def to_bytes(file):
  f = open(file, 'rb')
  f_bytes = base64.b64encode(f.read()).decode('utf8')
  return f_bytes

def getXmlValues(file):
  xml = open(file, 'r').read()
  xml = bytes(bytearray(xml, encoding='utf-8'))
  xml = etree.XML(xml)

  msg = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch/Message/Description').text
  msg_TypeName = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch/Message').attrib['TypeName']

  ba_id = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch').attrib['Id']
  ba_statId = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch').attrib['StatusId']
  ba_statName = xml.find('.//{http://www.w3.org/2003/05/soap-envelope}Body/{https://ws.creditinfo.com}UploadZippedDataResponse/{https://ws.creditinfo.com}UploadZippedDataResult/CigResult/Result/Batch').attrib['StatusName']
  return f'{msg_TypeName}: {msg}\nBatch: id {ba_id} status {ba_statId}\n{ba_statName}'
  

if __name__ == '__main__':
  res = getXmlValues('./responses/5_3581801921_1#2021-02-11#22-34-37-370.xml')
  print(res)