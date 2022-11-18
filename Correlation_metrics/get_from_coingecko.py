import seaborn as sns
from matplotlib import pyplot as plt
import requests
import datetime
import numpy as np
import sqlite3

'''

HERE WE GET INFO VARIATION FROM COINGECKO 
AND INSERT IN SQLITE DATABASE

'''

# CHOOSE THE CRYPTO TO COMPARE

print('')
crypto_1 = input('Choose the first crypto: ')
crypto_2 = input('Choose the second crypto: ')
crypto_id_1 = input('Insert the API id of firt crypto: ')
crypto_id_2 = input('Insert the API id of second crypto: ')
n_days = input('How many days do you want (n, max): ')

# GET THE HISTORICAL VALUES OF THE PRICE

    # First crypto

headers_1 = {
    'id' : crypto_id_1,
    'vs_currency' : 'usd',
    'days' : n_days,
    'interval' : 'daily'
}

url = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + headers_1['vs_currency'] +'&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

r_1 = requests.get(url)
response_1 = r_1.json()

size_of_list = len(response_1)
if size_of_list < 3:
    print('')
    print('Probably the id is wrong')
    print('Open this link to find the correct id: https://api.coingecko.com/api/v3/coins/list')
    print('')
    crypto_1 = input('Choose the crypto name 1: ')
    headers_1 = {
        'id': crypto_id_1,
        'vs_currency': 'usd',
        'days': n_days,
        'interval': 'daily'
    }

    url = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + \
          headers_1['vs_currency'] + '&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

    r_1 = requests.get(url)
    response_1 = r_1.json()

    # Second crypto

headers_2 = {
    'id' : crypto_id_2,
    'vs_currency' : 'usd',
    'days' : n_days,
    'interval' : 'daily'
}

url = 'https://api.coingecko.com/api/v3/coins/' + headers_2['id'] + '/market_chart?' + 'vs_currency=' + headers_2['vs_currency'] +'&days=' + headers_2['days'] + '&interval=' + headers_2['interval']

r_2 = requests.get(url)
response_2 = r_2.json()

size_of_list = len(response_2)
if size_of_list < 3:
    print('')
    print('Probably the id is wrong')
    print('Open this link to find the correct id: https://api.coingecko.com/api/v3/coins/list')
    print('')
    crypto_2 = input('Choose the crypto name 2: ')
    headers_2 = {
        'id': crypto_id_2,
        'vs_currency': 'usd',
        'days': n_days,
        'interval': 'daily'
    }

    url = 'https://api.coingecko.com/api/v3/coins/' + headers_2['id'] + '/market_chart?' + 'vs_currency=' + \
          headers_2['vs_currency'] + '&days=' + headers_2['days'] + '&interval=' + headers_2['interval']

    r_2 = requests.get(url)
    response_2 = r_2.json()

# FILTER VALUES

size_1 = len(response_1['prices'])
size_2 = len(response_2['prices'])

crypto_1_list = list()
crypto_2_list = list()

    # FIRST CRYPTO

for i in range(size_1):
    # GET VALUES

    date_value = response_1['prices'][i][0]
    price = response_1['prices'][i][1]

    # EXCEPTION TO ERRORS

    if price == None or price == 0:
        continue

    # FILTER DATE

    date = str(datetime.datetime.fromtimestamp(date_value / 1000)).split(' ')[0]

    # CREATE VAR. IN PRICE VALUE

    if i >1 :
        var = price / (response_1['prices'][i-1][1]) - 1
    else:
        var = 0

    # INSERT INTO LIST

    final_value = (date, price, var)
    crypto_1_list.append(final_value)

    # SECOND CRYPTO

for i in range(size_2):
    # GET VALUES

    date_value = response_2['prices'][i][0]
    price = response_2['prices'][i][1]

    # EXCEPTION TO ERRORS

    if price == None or price == 0:
        continue

    # FILTER DATE

    date = str(datetime.datetime.fromtimestamp(date_value / 1000)).split(' ')[0]

    # CREATE VAR. IN PRICE VALUE

    if i > 1:
        var = price / (response_2['prices'][i - 1][1]) - 1
    else:
        var = 0

    # INSERT INTO LIST

    final_value = (date, price, var)
    crypto_2_list.append(final_value)

print('')
# CREATE DATABASE IN SQL

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

update = input('Do you want delete the existence tables (yes/no): ')
if update == 'yes':
    cur.execute(
        '''DROP TABLE IF EXISTS {}'''.format(crypto_1)
    )

    cur.execute(
        '''DROP TABLE IF EXISTS {}'''.format(crypto_2)
    )
    conn.commit()

    print('-- DELETED COMPLETE --')

print('')
print('START CREATING TABLES AND INSERT VALUES --')

cur.execute(
    '''CREATE TABLE IF NOT EXISTS {} (
    date TEXT,
    price_var FLOAT)'''.format(crypto_1)
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS {} (
    date TEXT,
    price_var FLOAT)'''.format(crypto_2)
)
conn.commit()

var_1 = list()
date_1 = list()
for i in range(len(crypto_1_list)):
    v = crypto_1_list[i][2]
    var_1.append(v)

    d = crypto_1_list[i][0]
    date_1.append(d)

    cur.execute(
        '''INSERT INTO {} (date, price_var)
        VALUES (?,?)'''.format(crypto_1), (d, float(v))
    )
    conn.commit()

print('-- TABLE 1 -> INSERT COMPLETE')

var_2 = list()
date_2 = list()
for i in range(len(crypto_2_list)):
    v = crypto_2_list[i][2]
    var_2.append(v)

    d = crypto_2_list[i][0]
    date_2.append(d)

    cur.execute(
        '''INSERT INTO {} (date, price_var)
        VALUES (?,?)'''.format(crypto_2), (d, float(v))
    )
    conn.commit()

print('-- TABLE 2 -> INSERT COMPLETE ')
print('')

print('-- ITS COMPLETE --')





