import requests
import pprint
import datetime
import matplotlib.pyplot as plt
import numpy as np

'''
LINK TO FIND THE TOKEN ID IF YOU CAN'T FIND:
https://api.coingecko.com/api/v3/coins/list
'''

print('')
print('Important note -> Dont forget the name of the crypto is the API ID in coingecko')
print('')

# CHOOSE THE CRYPTO YOU WANT

crypto = input('Choose the crypto name: ')
n_days = input('How many days (number or max): ')

# GET THE HISTORICAL VALUES

headers_1 = {
    'id' : crypto,
    'vs_currency' : 'usd',
    'days' : n_days,
    'interval' : 'daily'
}

url = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + headers_1['vs_currency'] +'&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

r = requests.get(url)
response = r.json()

size_of_list = len(response)
if size_of_list < 3:
    print('')
    print('Probably the id is wrong')
    print('Open this link to find the correct id: https://api.coingecko.com/api/v3/coins/list')
    print('')
    crypto = input('Choose the crypto name: ')
    headers_1 = {
        'id': crypto,
        'vs_currency': 'usd',
        'days': n_days,
        'interval': 'daily'
    }

    url = 'https://api.coingecko.com/api/v3/coins/' + headers_1['id'] + '/market_chart?' + 'vs_currency=' + \
          headers_1['vs_currency'] + '&days=' + headers_1['days'] + '&interval=' + headers_1['interval']

    r = requests.get(url)
    response = r.json()


# pprint.pprint(response)

# FILTER THE VALUES

size_prices = len(response['prices'])
count = 0

cs_list = list()
date_list = list()

print('LOOP STARTS')

for i in range(size_prices):

    # print(i)

    # GET THE VALUES

    date_value = response['prices'][i][0]
    price = response['prices'][i][1]
    market_cap = response['market_caps'][i][1]
    total_volume = response['total_volumes'][i][1]

    # EXCEPTION TO ERRORS

    if price == None or market_cap == None or price == 0 or market_cap == 0:
        continue

    # FILTER DATA

        # DATE

    date = str(datetime.datetime.fromtimestamp(date_value / 1000)).split(' ')[0]
    # print(date,'//', price, market_cap, total_volume)

        # GET CIRCULATION SUPPLY

    cs = float(market_cap) / float(price)
    # print('Circulation supply: ', cs)

    # INSERT DATA IN LIST

    cs_list.append(int(cs))
    date_list.append(date)


    '''
    TIME TO WORK WITH THE DATABASE -- 1. VERIFY IF THE DATA ALREADY HAVE THIS INFO // 2. IF NOT INSERT THE NEW DATA
    '''

print('LOOP COMPLETED')
# print('Circulation supply list: ', cs_list)
# print(date_list)

# CREATE LOOP TO GET INFLATION MONTHLY

number_list = list()
number_list_1 = list()
y = 0
y_1 = 0
count = 0
count_1 = 0
st_cs = cs_list[0]
st_cs_1 = cs_list[0]
inflation_list = list()
inflation_list_1 = list()
sum_list = list()
sum_list_1 = list()
v_1 = 0
v = 0

for i in range(len(cs_list)):

    count += 1
    count_1 += 1

    if count_1 == 7:

        # VALUE

        inflation = cs_list[i] / st_cs_1 - 1

        if len(sum_list_1) == 0:
            v_1 = inflation
        else:
            v_1 += inflation

        # INSERT IN LIST

        y_1 += 1
        number_list_1.append(y_1)
        inflation_list_1.append(inflation)
        sum_list_1.append(v_1)


        # REPLACE START VALUES

        st_cs_1 = cs_list[i]
        count_1 = 0

    if count == 30:
        # VALUE

        inflation = cs_list[i] / st_cs - 1

        if len(sum_list) == 0:
            v = inflation
        else:
            v += inflation

        # INSERT IN LIST

        y += 1
        number_list.append(y)
        inflation_list.append(inflation)
        sum_list.append(v)

        # REPLACE START VALUES

        st_cs = cs_list[i]
        count = 0

# CREATE AVG VALUES

inflation_list_avg = [np.average(inflation_list)]*len(inflation_list)
inflation_list_avg_1 = [np.average(inflation_list_1)]*len(inflation_list_1)

# WRITE SOME VALUES

print('')
print('-- SOME VALUES ABOUT INFLATION --')
print('')
print('Avg of inflation per month: ', round(np.average(inflation_list) * 100, 3), '%')
print('Avg of inflation per week: ', round(np.average(inflation_list_1) * 100, 3), '%')
print('')
print('Median of inflation per month: ', round(np.median(inflation_list) * 100, 3), '%')
print('Median of inflation per week: ', round(np.median(inflation_list_1) * 100, 3), '%')
print('')
print('INFO ABOUT QUANTILES - monthly')
print(' - Q1: ', round(np.quantile(inflation_list,0.25) * 100, 3), '%')
print(' - Q3: ', round(np.quantile(inflation_list,0.75) * 100, 3), '%')
print('')
print('INFO ABOUT QUANTILES - weekly')
print(' - Q1: ', round(np.quantile(inflation_list_1,0.25) * 100, 3), '%')
print(' - Q3: ', round(np.quantile(inflation_list_1,0.75) * 100, 3), '%')
print('')
print('-- Lets see the graphs')
print('')


# CREATE GRAPH

plt.subplot(2,2,1)
plt.plot(date_list, cs_list)
plt.xlabel('Date')
plt.ylabel('Circulation supply')
plt.title('Token inflation')

plt.subplot(2,2,2)
plt.bar(number_list, inflation_list, width=0.8, color='black')
plt.plot(number_list, inflation_list_avg)
plt.xlabel('Number of months')
plt.ylabel('Inflation per month')
plt.title('Inflation per month for token')

plt.subplot(2,2,3)
plt.bar(number_list_1, inflation_list_1, width=0.8, color='black')
plt.plot(number_list_1, inflation_list_avg_1)
plt.xlabel('Number of weeks')
plt.ylabel('Inflation per week')
plt.title('Inflation per week for token')

plt.subplot(2,2,4)
plt.bar(number_list, sum_list, width=0.8, color='black')
plt.xlabel('Number of months')
plt.ylabel('Inflation per month')
plt.title('Sum Inflation per month for token')

plt.show()

print('DONE --')