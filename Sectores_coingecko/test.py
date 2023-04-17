import requests
import pprint
from tabulate import tabulate
import numpy as np
from datetime import datetime
import time


def make_request_with_rate_limit_handling(url):
    success = False
    while not success:
        response = requests.get(url)
        json_response = response.json()
        if 'error_message' in json_response:
            if "You've exceeded the Rate Limit" in json_response['error_message']:
                print("Rate limit exceeded. Waiting for 120 seconds.")
                time.sleep(120)
                continue
        success = True
    return json_response


print('')
print('-- Lets start sector algo ')
print('')

print('Important note -> The sector needs to be the coingecko sector id (you can run the other script to know the id)')
print('')

# Input
a = input('Pick a sector (id coingecko): ')

# Get data
url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=' + a + '&order=market_cap_desc&per_page=100&page=1&sparkline=false'
response = make_request_with_rate_limit_handling(url)

# Work data
name_l = list()
marketcap_l = list()
volume_l = list()
vol_marketcap_l = list()
data_for_table_l = list()
ticket_l = list()
fdv_l = list()
price_24h_changes_l = list()
token_launch_date_l = list()

for i in range(len(response)):
    name = response[i]['name']
    market_cap = round(float(response[i]['market_cap']), 3)
    volume = round(float(response[i]['total_volume']), 3)
    ticket = response[i]['symbol']
    coin_id = response[i]['id']  # Get the coin ID to request individual coin data

    # Get individual coin data to obtain genesis_date
    coin_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&community_data=false&developer_data=false'
    coin_response = make_request_with_rate_limit_handling(coin_url)

    try:
        token_launch_date = coin_response['genesis_date']
    except KeyError:
        token_launch_date = 'N/A'

    # If genesis_date is not available, use the first date from price chart
    if token_launch_date is None or not isinstance(token_launch_date, str):
        token_launch_date = 'N/A'

    try:
        datetime.strptime(token_launch_date, '%Y-%m-%d')
    except ValueError:
        success = False
        while not success:
            price_history_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=max&interval=daily'
            price_history_response = make_request_with_rate_limit_handling(price_history_url)

            if 'prices' in price_history_response and price_history_response['prices']:
                first_date = price_history_response['prices'][0][0] // 1000  # Convert to Unix timestamp (seconds)
                token_launch_date = datetime.utcfromtimestamp(first_date).strftime('%Y-%m-%d')
            else:
                token_launch_date = 'N/A'
            success = True

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

    a = (i, name, ticket, marketcap2, fdv2, volume2, vol_marketcap_r, price_24h_changes, token_launch_date)

    # Insert list

    name_l.append(name)
    marketcap_l.append(market_cap)
    volume_l.append(volume)
    vol_marketcap_l.append(vol_marketcap_r)
    ticket_l.append(ticket)
    fdv_l.append(fdv)
    price_24h_changes_l.append(price_24h_changes)
    token_launch_date_l.append(token_launch_date)

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
        '24h Changes %',
        'Token Launch Date'
    ]
    print(tabulate(data_for_table_l, headers=head, tablefmt='grid'))

q1 = input('Do you wanna order by MCap 24h % (yes/no): ')
if q1 == 'yes':
    sorted_list = sorted(data_for_table_l, key=lambda x: x[7])
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
    print(tabulate(sorted_list, headers=head, tablefmt='grid'))
