import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pprint

'''
LINK TO FIND THE TOKEN ID IF YOU CAN'T FIND:
https://api.coingecko.com/api/v3/coins/list
'''

print('')
print('Important note -> Dont forget the name of the crypto is the API ID in coingecko')
print('')

# CHOOSE THE CRYPTO YOU WANT

crypto = input('Choose the crypto name: ')
interval = input('Choose the interval (daily/hourly): ')
if interval == 'hourly':
    print('(Choose days < 90)')
n_days = input('How many days (number or max): ')


# CREATE THE REQUEST

    # FIRST REQUEST - GET THE PRICE OF ASSET

headers_1 = {
    'id': crypto,
    'vs_currency' : 'usd',
    'days': n_days,
    'interval': interval
}

url_1 = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + headers_1['vs_currency'] +'&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

r_1 = requests.get(url_1)
response_1 = r_1.json()

    # SECOND REQUEST - GET THE TOTAL SUPPLY

url_2 = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'

r_2 = requests.get(url_2)
response_2 = r_2.json()

# GET THE TOTAL SUPPLY

print('')
print('-- MACRO VALUES --')
print('')
market_cap = float(response_2['market_data']['market_cap']['usd'])
print('Market cap: {0:12,.3f}'.format(market_cap))
ath_market_cap = 0
for i in range(len(response_1['market_caps'])):
    a = float(response_1['market_caps'][i][1])
    if a > ath_market_cap:
        ath_market_cap = a
print('ATH Market Cap: {0:12,.3f}'.format(ath_market_cap))
print('')
circ_supply = float(response_2['market_data']['circulating_supply'])
print('Circulation supply: {0:12,.3f}'.format(circ_supply))
total_supply = float(response_2['market_data']['total_supply'])
print('Total supply: {0:12,.3f}'.format(total_supply))
max_supply = response_2['market_data']['max_supply']
try:
    print('Max supply: {0:12,.3f}'.format(float(max_supply)))
except:
    print('Max supply: None')

try:
    perc_burning = ( float(max_supply) - float(total_supply) ) / float(max_supply) * 100
    print('Percentage of burning: {0:12,.3f}'.format(perc_burning), '%')
except:
    print('Percentage of burning: ?')

try:
    perc_outside_tokes = (circ_supply / total_supply) * 100
    print('Percentage of outside tokens: {0:12,.3f}'.format(perc_outside_tokes), '%')
except:
    print('Percentage of oustide tokens: ?')

# GET THE PRICE

fdv_list = list()
date_list = list()

print('')
print('-- START LOOPING THE DATA --')
for i in range(len(response_1['prices'])):

    # GET VALUES

    date_value = response_1['prices'][i][0]
    price = response_1['prices'][i][1]

    # EXCEPTION TO ERRORS

    if price == None or price == 0:
        continue

    # CALC. THE FDV

    fdv = float(price) * total_supply

    # FILTER THE DATE

    date = str(datetime.datetime.fromtimestamp(date_value / 1000)).split(' ')[0] + ' ' + str(datetime.datetime.fromtimestamp(date_value / 1000)).split(' ')[1].split(':')[0] + 'h'

    # INSERT VALUES IN LISTS

    fdv_list.append(fdv)
    date_list.append(date)

print('LOOP COMPLETED')
print('')

# GET THE FINAL FDV

print('-- INFO ABOUT FDV -- ')
print('')
fdv_actual = fdv_list[-1]
print('Actual FDV: {0:12,.3f}'.format(fdv_actual))
fdv_ath = max(fdv_list)
print('ATH FDV: {0:12,.3f}'.format(fdv_ath))
perc_down_ath = round(float((fdv_actual / fdv_ath - 1) * 100),3)
print('Perc down from ATH: ', perc_down_ath, '%')
to_ath = round(float(fdv_ath / fdv_actual),3)
print('How many x to ATH: ', to_ath, 'x')
print('')

a = input('Do you want to see the chart (yes/no): ')
if a == 'yes':
    plt.plot(date_list, fdv_list)
    plt.xlabel('Date')
    plt.ylabel('FDV')
    plt.title('FDV w/ the last total supply')
    plt.show()

    aa = input('Do you wanna see log chart (yes/no): ')
    if aa == 'yes':
        plt.plot(date_list, fdv_list)
        plt.yscale('log')
        plt.xlabel('Date')
        plt.ylabel('FDV')
        plt.title('FDV w/ the last total supply')
        plt.show()

print('')
print(' -- ITS COMPLETED --')



