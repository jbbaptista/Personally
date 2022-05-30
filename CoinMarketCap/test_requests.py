import requests
import pprint

 # Choose the crypto you want

crypto = input('Choose the crypto name: ')

 # Get the actual price for picked crypto

headers = {
    'ids' : crypto,
    'vs_currencies' : 'usd',
}

url = 'https://api.coingecko.com/api/v3/simple/price' + '?' + 'ids=' + headers['ids'] + '&vs_currencies=' + headers['vs_currencies'] + '&include_market_cap=true'

r = requests.get(url)
response = r.json()[crypto]

print(str(crypto) + ' price: ' + str(response['usd']))
print(str(crypto) + ' market cap: ' + str(response['usd_market_cap']))

 # Get historical price for picked coin

headers_1 = {
    'id' : crypto,
    'vs_currency' : 'usd',
    'days' : '10'
}

url = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + headers_1['vs_currency'] +'&days=' + headers_1['days']

r = requests.get(url)
response = r.json()

pprint.pprint(response)

value = response['prices'][0][1]
print(value)



