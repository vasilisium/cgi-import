import os
from aiohttp import ClientSession
import asyncio
from datetime import datetime
from ntpath import basename

from utils import toBase64, formatXML

import config
log = config.logger

url = 'https://test2.credithistory.com.ua/DataPump/Service.asmx'

def getRequestArgs(usr, pwd, zipBytes=''):
  return {
    'headers': {'content-type': 'text/xml'},
    'data': f"""
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Header>
    <CigWsHeader xmlns="https://ws.creditinfo.com">
      <UserName>{usr}</UserName>
      <Password>{pwd}</Password>
      <Version>4.0.0.0</Version>
      <Culture>en-GB</Culture>
      <UserId>10394</UserId>
    </CigWsHeader>
  </soap12:Header>
  <soap12:Body>
    <UploadZippedData xmlns="https://ws.creditinfo.com">
      <zippedXML>{zipBytes}</zippedXML>
      <schemaId>26</schemaId>
    </UploadZippedData>
  </soap12:Body>
</soap12:Envelope>
    """
  }

def removeCredentials(data):
  # TODO: removeCredentials from output xml file
  return data


def writeXml(fileName, data):
  dt = datetime.now().strftime('%Y-%m-%d#%H-%M-%S-%f')[:-3]
  new_file_name = f'./responses/{fileName}#{dt}.xml'
  if not os.path.exists(os.path.dirname(new_file_name)):
    os.makedirs(os.path.dirname(new_file_name))
  
  with open(new_file_name, 'w') as xml:
    new_data = removeCredentials(data)
    xml.write(new_data)

  return new_file_name

# def makeZip(xmlFile):
#   # TODO: create zip from xml or just return zip
#   return ''

async def req(session, zip):
  # zip = makeZip(zip)

  async with ClientSession() as session:
    req_args = getRequestArgs(config.USR, config.PWD, zip)
    async with session.post(url, **req_args) as res:
      return await res.text()
      

async def post(zip):
  async with ClientSession() as session:
    req_args = getRequestArgs(config.USR, config.PWD, zip)
    # req_args = getRequestArgs(config.USR, config.PWD, zip)
    async with session.post(url, data=req_args['data'], headers=req_args['headers']) as resp:
      resp_text = await resp.text()
      return [resp.status, resp_text]
  

async def post_all(loop, zips=[]):
  async with ClientSession(loop=loop) as session:
    data = await asyncio.gather(*[req(session, zip) for zip in zips], return_exceptions=True)
    return data

def doWork(zip_bytes):

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

  # loop = asyncio.get_event_loop()
  datas = loop.run_until_complete(post_all(loop, zips=[zip_bytes]))
  for data in datas:
    writeXml(removeCredentials(data))

def send_zip(zipFile):
  zip_data = toBase64(zipFile)

  # loop = asyncio.get_event_loop()
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  res = loop.run_until_complete(post(zip_data))

  filename = basename(zipFile)
  filename = os.path.splitext(filename)[0]

  normalizedXML = formatXML(res[1])
  resultXML = writeXml(filename, normalizedXML)
  res[1] = resultXML
  log.info('%s Posted with status %s and response in file %s', filename, res[0], resultXML)
  
  return res

if __name__ == '__main__': 
  doWork()