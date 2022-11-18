import requests
import pprint

crypto = input('Crypto name (coingecko): ')

url = 'http://api.llama.fi/protocols'

r = requests.get(url)
response = r.json()

# PROCURAR O SLUG NO DEFILLAMA VIA COINGECKO

b = 0
for i in range(len(response)):

    v = response[i]['gecko_id']

    if v == crypto:
        print(v)
        b = i

slug = response[b]['slug']
print(slug)


