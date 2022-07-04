import requests
import json
import pprint

url = 'http://pro-api.coinmarketcap.com/v1/cryptocurrency/categories'
key = '14c2bc3e-3dda-493b-9948-248716c75b37'

headers = {
  'Accepts' : 'application/json',
  'X-CMC_PRO_API_KEY' : key,
}

session = requests.session()
session.headers.update(headers)

try:
  response = session.get(url)
  data = json.loads(response.text)
  pprint.pprint(data)
except (ConnectionError, TimeoutError) as e:
  print(e)
