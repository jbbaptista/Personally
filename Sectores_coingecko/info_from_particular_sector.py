import requests
import pprint
from tabulate import tabulate
import numpy as np

print('')
print('-- Lets start sector algo ')
print('')

print('Important note -> The sector needs to be the coingecko sector id (you can run the other script to know the id)')
print('')

# Input

a = input('Pick a sector (id coingecko): ')

# Get data

url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=' + a + '&order=market_cap_desc&per_page=100&page=1&sparkline=false'

r = requests.get(url)
response = r.json()

# Work data

name_l = list()
marketcap_l = list()
volume_l = list()
vol_marketcap_l = list()
data_for_table_l = list()
ticket_l = list()
fdv_l = list()
price_24h_changes_l = list()

for i in range(len(response)):

    name = response[i]['name']
    market_cap = round(float(response[i]['market_cap']), 3)
    volume = round(float(response[i]['total_volume']), 3)
    ticket = response[i]['symbol']
    try:
        price_24h_changes = round(float(response[i]['price_change_percentage_24h']), 3)
    except:
        price_24h_changes = 0
    try:
        fdv = round(float(response[i]['fully_diluted_valuation']), 3)
    except:
        fdv = 0

    try:
        vol_marketcap_r = round(volume / market_cap * 100, 2)
    except:
        vol_marketcap_r = 0

    if market_cap / 1000000 < 1000:
        marketcap2 = str(round(market_cap / 1000000, 3)) + ' M'
    else:
        marketcap2 = str(round(market_cap/1000000000, 3)) + ' B'

    if volume / 1000000 < 1000:
        volume2 = str(round(volume / 1000000, 3)) + ' M'
    else:
        volume2 = str(round(volume / 1000000000, 3)) + ' B'

    if fdv / 1000000 < 1000:
        fdv2 = str(round(fdv / 1000000, 3)) + ' M'
    else:
        fdv2 = str(round(fdv / 1000000000, 3)) + ' B'

    a = (i, name, ticket, marketcap2, fdv2, volume2, vol_marketcap_r, price_24h_changes)

    # Insert list

    name_l.append(name)
    marketcap_l.append(market_cap)
    volume_l.append(volume)
    vol_marketcap_l.append(vol_marketcap_r)
    ticket_l.append(ticket)
    fdv_l.append(fdv)
    price_24h_changes_l.append(price_24h_changes)

    data_for_table_l.append(a)

# Data values

avg = round(float(np.average(marketcap_l)), 3)
if avg / 1000000 < 1000:
    avg1 = str(round(avg / 1000000, 3)) + ' M'
else:
    avg1 = str(round(avg/ 1000000000, 3)) + ' B'

avg_fdv = round(float(np.average(fdv_l)), 3)
if avg_fdv / 1000000 < 1000:
    avg_fdv1 = str(round(avg_fdv / 1000000, 3)) + ' M'
else:
    avg_fdv1 = str(round(avg_fdv/ 1000000000, 3)) + ' B'

median = np.median(marketcap_l)
if median / 1000000 < 1000:
    median1 = str(round(median / 1000000, 3)) + ' M'
else:
    median1 = str(round(median/ 1000000000, 3)) + ' B'

median_fdv = np.median(fdv_l)
if median_fdv / 1000000 < 1000:
    median_fdv1 = str(round(median_fdv / 1000000, 3)) + ' M'
else:
    median_fdv1 = str(round(median_fdv/ 1000000000, 3)) + ' B'

print('')
print('Avg MarketCap: ', avg1)
print('Median MarketCap: ', median1)
print('')
print('Avg FDV: ', avg_fdv1)
print('Median FDV: ', median_fdv1)
print('')

# Graphs and tables

b = input('Do you wanna see the table (yes/no): ')
if b == 'yes':
    head = [
        'Nº',
        'Cryptos',
        'Ticket',
        'MarketCap',
        'Fdv',
        'Volume 24h',
        'Vol/MCap %',
        '24h Changes %'
    ]
    print(tabulate(data_for_table_l, headers=head, tablefmt='grid'))


