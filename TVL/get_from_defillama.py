import requests
import datetime
import numpy as np
from matplotlib import pyplot as plt
import pprint

'''

THE GOAL IS TO GET TVL CHART FROM DEFILLAMA
AND MARKET CAP FROM COINGECKO

'''

print('')
# SELECT THE CRYPTO

crypto = input('Crypto name (coingecko API name): ')

# FIND WHAT IS THE SLUG IN DEFILLAMA

urll = 'http://api.llama.fi/protocols'

rr = requests.get(urll)
respp = rr.json()

b = 0

for i in range(len(respp)):
    v = respp[i]['gecko_id']

    if v == crypto:
        b = i

crypto_name = respp[b]['slug']

if b == 0:
    print('')
    print('-- DOESNT FIND THE SLUG IN DEFILLAMA -> PROBABLY THE TOKEN DOESNT EXIST --')
    print('YOU CAN CHECK IN http://api.llama.fi/protocols ')
    print('')
    exit()

print('')

# CREATE THE REQUEST

url = 'https://api.llama.fi/protocol/' + crypto_name

r_1 = requests.get(url)
resp = r_1.json()

response_1 = resp['tvl']

print('-- START LOOPING THE DATA --')

# LOOPS

date_l = list()
tvl_l = list()
data_1 = list()
for i in range(len(response_1)):
    # GET VALUES

    date = int(response_1[i]['date'])
    tvl = float(response_1[i]['totalLiquidityUSD'])

    if tvl == None or tvl == 0:
        continue

    # MANIPULATE THE DATA

    date1 = str(datetime.datetime.fromtimestamp(date)).split(' ')[0]

    # INSERT THE VALUES IN LISTS

    date_l.append(date1)
    tvl_l.append(tvl)
    a = (date1, tvl)
    data_1.append(a)


# GET MARKET CAP FROM COINGECKO

headers_1 = {
    'id': crypto,
    'vs_currency' : 'usd',
    'days': 'max',
    'interval': 'daily'
}

url_2 = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + headers_1['vs_currency'] +'&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

r_2 = requests.get(url_2)
response_2 = r_2.json()

date_list = list()
market_cap_list = list()
data_2 = list()
for i in range(len(response_2['market_caps'])):

    # GET VALUES

    date_value = response_2['market_caps'][i][0]
    market_cap = response_2['market_caps'][i][1]

    # EXCEPTION TO ERRORS

    if market_cap == None or market_cap == 0:
        continue

    # FILTER THE DATE

    date = str(datetime.datetime.fromtimestamp(date_value / 1000)).split(' ')[0]

    # INSERT VALUES IN LISTS

    market_cap_list.append(market_cap)
    date_list.append(date)
    a = (date, market_cap)
    data_2.append(a)

print('LOOP COMPLETED')

# CREATE CDATA FOR RATIO TVL / MARKETCAP

r_tvl_marketcap = list()
date_r = list()

for i in range(len(data_1)):
    d = data_1[i][0]

    for a in range(len(data_2)):
        v = data_2[a][0]
        if d == v:

            # GET VALUES

            tvl = data_1[i][1]
            marketcap = data_2[a][1]

            r = round(float(tvl) / float(marketcap),3)

            # INSERT IN ANOTHER LIST

            r_tvl_marketcap.append(r)
            date_r.append(v)

            break

# MANIPULATE DATA

print('')
print('-- TVL INFO -- ')
print('')

max_tvl = max(tvl_l)
print('ATH for TVL: {0:12,.3f}'.format(max_tvl))
actual_tvl = tvl_l[-1]
print('Actual TVL: {0:12,.3f}'.format(actual_tvl))
perc_down = round((float(actual_tvl) / float(max_tvl) - 1) * 100, 2)
print('Percentage down from ATH: ', perc_down, '%')

print('')
print('-- MARKET CAP INFO -- ')
print('')

max_marketcap = max(market_cap_list)
print('ATH for Market cap {0:12,.3f}'.format(max_marketcap))
actual_marketcap = market_cap_list[-1]
print('Actual Marketcap: {0:12,.3f}'.format(actual_marketcap))
perc_down_marketcap = round((float(actual_marketcap) / float(max_marketcap) - 1) * 100, 2)
print('Perc down from ATH Marketcap: ', perc_down_marketcap, '%')
ratio_max_marketcap = round(max(r_tvl_marketcap), 3)

print('')
print('-- TVL / MARKET CAP INFO --')
print('')

print('ATH ratio for TVL / Marketcap: ', ratio_max_marketcap)
ratio_actual_marketcap = round(r_tvl_marketcap[-1], 3)
print('Actual ratio for TVL / Marketcap: ', ratio_actual_marketcap)
perc_down_ratio = round((ratio_actual_marketcap / ratio_max_marketcap - 1) * 100, 2)
print('Perc down from ATH ratio: ', perc_down_ratio, '%')

'''
FAZER VARIOS RATIOS COM O MARKET CAP
E GRAFICO PARA MARKET CAP  / TVL
'''

# CREATE A CHART FOR TVL

print('')
print('-- LETS SEE THE CHARTS')
a = input('Do you wanna see charts (yes/no): ')
print('')

if a == 'yes':
    plt.plot(date_l, tvl_l)
    plt.xlabel('Date')
    plt.ylabel('TVL')
    plt.title('TVL historical')
    plt.show()

    plt.plot(date_r, r_tvl_marketcap)
    plt.xlabel('Date')
    plt.ylabel('TVL / Marketcap')
    plt.title('Ratio for TVL / Marketcap historical')
    plt.show()

print('DONE --')





