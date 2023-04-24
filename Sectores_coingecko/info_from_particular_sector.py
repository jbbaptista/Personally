import requests
import pprint
from tabulate import tabulate
import numpy as np
from datetime import datetime
import time

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

print('\n-- Start Looping\n')
for i in range(len(response)):

    name = response[i]['name']
    market_cap = round(float(response[i]['market_cap']), 3)
    volume = round(float(response[i]['total_volume']), 3)
    ticket = response[i]['symbol']
    id = response[i]['id']
    print(i, ':', name,'//',market_cap,'//',volume)

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
        marketcap2 = str(round(market_cap / 1000000000, 3)) + ' B'

    if volume / 1000000 < 1000:
        volume2 = str(round(volume / 1000000, 3)) + ' M'
    else:
        volume2 = str(round(volume / 1000000000, 3)) + ' B'

    if fdv / 1000000 < 1000:
        fdv2 = str(round(fdv / 1000000, 3)) + ' M'
    else:
        fdv2 = str(round(fdv / 1000000000, 3)) + ' B'

    # Get the first date value

    try:
        url1 = 'https://api.coingecko.com/api/v3/coins/' + id + '/market_chart?vs_currency=usd&days=max'
        r1 = requests.get(url1)
        response1 = r1.json()['prices'][0][0]
        launch_date = datetime.fromtimestamp(response1 / 1000).strftime('%Y-%m-%d')
        r1.raise_for_status()
    except:
        print('')
        print('Exceeded rate limit - Waiting 120sec to continue')
        time.sleep(120)
        print('-- Continue')
        print('')
        url1 = 'https://api.coingecko.com/api/v3/coins/' + id + '/market_chart?vs_currency=usd&days=max'
        r1 = requests.get(url1)
        response1 = r1.json()['prices'][0][0]
        launch_date = datetime.fromtimestamp(response1 / 1000).strftime('%Y-%m-%d')

    today_day = datetime.today().strftime('%Y-%m-%d')
    a = datetime.strptime(launch_date, '%Y-%m-%d').date()
    b = datetime.strptime(today_day, '%Y-%m-%d').date()
    number_of_days = str((b - a).days) + 'D'

    # Final value to table

    a = (i, name, ticket, marketcap2, fdv2, volume2, vol_marketcap_r, price_24h_changes, launch_date, number_of_days)

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
    avg1 = str(round(avg / 1000000000, 3)) + ' B'

avg_fdv = round(float(np.average(fdv_l)), 3)
if avg_fdv / 1000000 < 1000:
    avg_fdv1 = str(round(avg_fdv / 1000000, 3)) + ' M'
else:
    avg_fdv1 = str(round(avg_fdv / 1000000000, 3)) + ' B'

median = np.median(marketcap_l)
if median / 1000000 < 1000:
    median1 = str(round(median / 1000000, 3)) + ' M'
else:
    median1 = str(round(median / 1000000000, 3)) + ' B'

median_fdv = np.median(fdv_l)
if median_fdv / 1000000 < 1000:
    median_fdv1 = str(round(median_fdv / 1000000, 3)) + ' M'
else:
    median_fdv1 = str(round(median_fdv / 1000000000, 3)) + ' B'

print('\n-- GLOBAL INFO --\n')
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
        '24h Changes %',
        'Launch Date',
        'Days'
    ]
    print(tabulate(data_for_table_l, headers=head, tablefmt='grid'))

q1 = input('Do you wanna order by MCap 24h % (yes/no): ')
if q1 == 'yes':
    sorted_list = sorted(data_for_table_l, key=lambda x: x[7], reverse=True)
    head = [
        'Nº',
        'Cryptos',
        'Ticket',
        'MarketCap',
        'Fdv',
        'Volume 24h',
        'Vol/MCap %',
        '24h Changes %',
        'Launch date',
        'Days'
    ]
    print(tabulate(sorted_list, headers=head, tablefmt='grid'))


