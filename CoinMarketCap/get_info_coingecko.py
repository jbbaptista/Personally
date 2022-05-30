import requests
import pprint
import datetime

# CHOOSE THE CRYPTOYOU WANT

crypto = input('Choose the crypto name: ')

# GET THE HISTORICAL VALUES

headers_1 = {
    'id' : crypto,
    'vs_currency' : 'usd',
    'days' : '10',
    'interval' : 'daily'
}

url = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + headers_1['vs_currency'] +'&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

r = requests.get(url)
response = r.json()

pprint.pprint(response)

# FILTER THE VALUES

size_prices = len(response['prices'])
count = 0

for i in response['prices']:

    # NOW WHERE WE ARE

    count += 1

    # EXCEPTION FOR THE LAST VALUE BC ITS THE ACTUAL DAY VALUE

    if count == size_prices:
        print('DONE')
        break

    # GET THE VALUES

    date_value = i[0]
    price = i[1]

    # FILTER DATA

    date = datetime.datetime.fromtimestamp(date_value / 1000)
    # print(date,'//', price)

size_market_cap = len(response['market_caps'])
print(size_market_cap)

print(response['market_caps'])



