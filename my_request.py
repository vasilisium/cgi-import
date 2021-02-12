import requests

from config import USR, PWD, url

headers = {'content-type': 'text/xml'}
body = lambda zipData: f"""
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Header>
    <CigWsHeader xmlns="https://ws.creditinfo.com">
      <UserName>{USR}</UserName>
      <Password>{PWD}</Password>
      <Version>4.0.0.0</Version>
      <Culture>en-GB</Culture>
      <UserId>10394</UserId>
    </CigWsHeader>
  </soap12:Header>
  <soap12:Body>
    <UploadZippedData xmlns="https://ws.creditinfo.com">
      <zippedXML>{zipData}</zippedXML>
      <schemaId>26</schemaId>
    </UploadZippedData>
  </soap12:Body>
</soap12:Envelope>
"""
def post(zipData):
  response = requests.post(url, headers=headers, data=body(zipData))
  return [response.status_code, response.text]

if __name__ == '__main__':
  from utils import writeXml, formatXML, getXmlValues, toBase64, zip, zip1
  # zipF = zip1('./xml/3_3222222218.xml')
  # data = toBase64(zipF)
  resp = post('data')
  xml = formatXML(resp[1])
  xml = writeXml('mock', xml)
  xml = open(xml,'r').read()
  # res = getXmlValues(xml)
  # print(res)