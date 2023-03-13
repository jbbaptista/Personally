import requests
import pprint
import datetime
import matplotlib.pyplot as plt

'''

GET INFO FOM COINGECKO
RECEIVED MARKETCAP FOR 2 DIFFERENT ASSETS 
COMPARE THE 2 ASSETS - GET A RATIO

'''

print('')
print('Important note -> Dont forget the name of the crypto is the API ID in coingecko')
print('')

# CHOOSE THE CRYPTO TO COMPARE

crypto1 = input('First crypto name: ')
crypto2 = input('Second crypto name: ')

print('')

# GET DATA FROM COINGECKO

    # REQUEST FOR CRYPTO 1

headers_1 = {
    'id': crypto1,
    'vs_currency' : 'usd',
    'days': 'max',
    'interval': 'daily'
}

url_1 = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + headers_1['vs_currency'] +'&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

r_1 = requests.get(url_1)
response_1 = r_1.json()

    # REQUEST FOR CRYPTO 2

headers_2 = {
    'id': crypto2,
    'vs_currency' : 'usd',
    'days': 'max',
    'interval': 'daily'
}

url_2 = 'https://api.coingecko.com/api/v3/coins/' + headers_2['id'] + '/market_chart?' + 'vs_currency=' + headers_2['vs_currency'] +'&days=' + headers_2['days'] + '&interval=' + headers_2['interval']

r_2 = requests.get(url_2)
response_2 = r_2.json()

# FILTER THE INFO

v1_list = list()
v2_list = list()
v1_price_list = list()
v2_price_list = list()
d_list = list()
ratio_list = list()
for i in range(len(response_1['market_caps'])):
    try:
        v1 = round(float(response_1['market_caps'][i][1]), 3)
    except:
        v1 = 0
    try:
        v3 = round(float(response_1['prices'][i][1]), 3)
    except:
        v3 = 0
    d1 = str(datetime.datetime.fromtimestamp(response_1['market_caps'][i][0] / 1000)).split(' ')[0]

    for i in range(len(response_2['market_caps'])):
        try:
            v2 = round(float(response_2['market_caps'][i][1]), 3)
        except:
            v2 = 0
        try:
            v4 = round(float(response_2['prices'][i][1]), 3)
        except:
            v4=0
        d2 = str(datetime.datetime.fromtimestamp(response_2['market_caps'][i][0] / 1000)).split(' ')[0]

        if d2 == d1:

            try:
                r = round(float(v1 / v2), 4)
            except:
                r = 0

            # INSERT VALUES IN LIST

            v1_list.append(v1)
            v2_list.append(v2)
            v1_price_list.append(v3)
            v2_price_list.append(v4)
            d_list.append(d1)
            ratio_list.append(r)

# PRINT SOME VALUES

print('Values for MarketCap ratio between : ', str(crypto1), ' / ', str(crypto2))
print('')
ratio_max = max(ratio_list)
print('Max ratio: ', ratio_max)
actual_ratio = ratio_list[-1]
print('Actual ratio: ', actual_ratio)
print('')

# CREATE GRAPH WITH THIS 2 VALUES

a = input('Graph for marketcap ratio (yes/no): ')
if a == 'yes':
    title = 'MarketCap ratio : ' + str(crypto1) + ' / ' + str(crypto2)
    plt.plot(d_list, ratio_list)
    plt.xlabel('Date')
    plt.title(title)
    plt.show()

print('')
# GET THE SAME RATIO BUT WITH FDV VALUES

url_3 = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'
url_4 = 'https://api.coingecko.com/api/v3/coins/' + headers_2['id'] + '?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'


r_3 = requests.get(url_3)
total_supply_1 = round(float(r_3.json()['market_data']['total_supply']), 2)

r_4 = requests.get(url_4)
total_supply_2 = round(float(r_4.json()['market_data']['total_supply']), 2)

fdv_1_list = list()
fdv_2_list = list()
fdv_ratio_list = list()
for i in range(len(v1_price_list)):
    try:
        v1 = round(float(v1_price_list[i]), 3)
    except:
        v1 = 0
    try:
        v2 = round(float(v2_price_list[i]), 3)
    except:
        v2 = 0

    # GET VALUES

    fdv1 = total_supply_1 * v1
    fdv2 = total_supply_2 * v2

    r = round(fdv1 / fdv2, 4)

    # INSERT IN THE LIST

    fdv_1_list.append(fdv1)
    fdv_2_list.append(fdv2)
    fdv_ratio_list.append(r)

# PRINT SOME VALUES

print('Values for FDV ratio between : ', str(crypto1), ' / ', str(crypto2))
print('')
v_max = max(fdv_ratio_list)
print('Max value: ', v_max)
actual_value = fdv_ratio_list[-1]
print('Actual value: ', actual_value)
print('')

# GRAPH WITH FDV VALUES

b = input('Graph for fdv ratio (yes/no): ')
if b == 'yes':
    title = 'FDV for the ratio : ' + str(crypto1) + ' / ' + str(crypto2)
    plt.plot(d_list, fdv_ratio_list)
    plt.xlabel('Date')
    plt.title(title)
    plt.show()


print('')

print('--DONE')
print('')







