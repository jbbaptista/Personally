import requests
import pprint
import datetime
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

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

aaa = 0
weekly_price_l = list()

aaa2 = 0
monthly_price_l = list()
for i in range(size_prices):
    aaa += 1
    aaa2 += 1
    # print(i)

    # GET THE VALUES

    date_value = response['prices'][i][0]
    price = response['prices'][i][1]
    market_cap = response['market_caps'][i][1]
    total_volume = response['total_volumes'][i][1]

    # EXCEPTION TO ERRORS

    if price == None or market_cap == None or price == 0 or market_cap == 0:
        aaa -= 1
        aaa2 -= 1
        continue

    # WEEKLY PRICE

    if aaa == 7:
        weekly_price_l.append(price)
        aaa = 0

    # MONTHLY PRICE

    if aaa2 == 30:
        monthly_price_l.append(price)
        aaa2 = 0

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
sum_daily_list = list()
daily_inflation_list = list()
number_daily_list = list()
avg_daily_list = list()
avg_weekly_list = list()
avg_monthly_list = list()
new_tokens_7_list = list()
new_tokens_30_list = list()
value_new_tokens_7_list = list()
value_new_tokens_30_list = list()
v_1 = 0
v = 0
v2 = 0
data_for_table_list = list()
data_for_table_list_monthly = list()

for i in range(len(cs_list)):

    count += 1
    count_1 += 1

    if i >0:
        daily_inflation = cs_list[i] / cs_list[i-1] - 1
    if i == 0:
        daily_inflation = 0

    # GET SOME VALUES

    if i == 0 :
        daily_sum = daily_inflation
        sum_daily_list.append(daily_sum)
        avg_daily_list.append(daily_sum)
    if i > 0:
        daily_sum = daily_inflation + float(sum_daily_list[-1])
        avg_daily = round(daily_sum / (len(sum_daily_list) + 1), 3)
        sum_daily_list.append(daily_sum)
        avg_daily_list.append(avg_daily)


    # INSERT IN LIST

    daily_inflation_list.append(daily_inflation)
    number_daily_list.append(i)


    if count_1 == 7:

        # VALUE

        inflation = cs_list[i] / st_cs_1 - 1

        new_tokens_7 = cs_list[i] - st_cs_1
        price_v = weekly_price_l[y_1]

        new_tokens_in_dollares = price_v * new_tokens_7

        if len(sum_list_1) == 0:
            v_1 = inflation
            avg_weekly_v = round(v_1, 3)
        else:
            v_1 += inflation
            avg_weekly_v = round(v_1 / (len(sum_list_1) + 1), 3)

        # INSERT IN LIST

        y_1 += 1
        number_list_1.append(y_1)
        inflation_list_1.append(inflation)
        sum_list_1.append(v_1)
        avg_weekly_list.append(avg_weekly_v)
        new_tokens_7_list.append(new_tokens_7)
        value_new_tokens_7_list.append(new_tokens_in_dollares)

        v_for_table = (y_1, new_tokens_7, new_tokens_in_dollares)
        data_for_table_list.append(v_for_table)


        # REPLACE START VALUES

        st_cs_1 = cs_list[i]
        count_1 = 0

    if count == 30:
        # VALUE

        inflation = cs_list[i] / st_cs - 1
        inflation_sum_i = cs_list[i] / cs_list[0] - 1

        new_tokens_30 = cs_list[i] - st_cs
        price_v = monthly_price_l[y]

        new_tokens_in_dollares = price_v * new_tokens_30

        if len(sum_list) == 0:
            v = inflation_sum_i
            v2 = inflation
            avg_monthly_v = round(inflation, 3)
        else:
            v += inflation_sum_i
            v2 += inflation
            avg_monthly_v = round(v2 / (len(avg_monthly_list) + 1), 3)


        # INSERT IN LIST

        y += 1
        number_list.append(y)
        inflation_list.append(inflation)
        sum_list.append(inflation_sum_i)
        avg_monthly_list.append(avg_monthly_v)
        new_tokens_30_list.append(new_tokens_30)
        value_new_tokens_30_list.append(new_tokens_in_dollares)

        v_for_table = (y, new_tokens_30, new_tokens_in_dollares)
        data_for_table_list_monthly.append(v_for_table)

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
print('Avg of inflation per week: ', round(np.average(inflation_list_1) * 100, 3), '%')
print('Avg of inflation per month: ', round(np.average(inflation_list) * 100, 3), '%')
print('')
print('Median of inflation per week: ', round(np.median(inflation_list_1) * 100, 3), '%')
print('Median of inflation per month: ', round(np.median(inflation_list) * 100, 3), '%')
print('')
print('Avg of Qt tokens released per week: {:,}'.format(round(np.average(new_tokens_7_list), 3)))
print('Avg of Qt tokens released per month: {:,}'.format(round(np.average(new_tokens_30_list), 3)))
print('')
print('Avg of tokens released in $ per week: {:,}'.format(round(np.average(value_new_tokens_7_list), 3)), '$')
print('Avg of tokens released in $ per month: {:,}'.format(round(np.average(value_new_tokens_30_list), 3)), '$')
print('')
print('INFO ABOUT QUANTILES - monthly')
print(' - Q1: ', round(np.quantile(inflation_list,0.25) * 100, 3), '%')
print(' - Q3: ', round(np.quantile(inflation_list,0.75) * 100, 3), '%')
print('')
print('INFO ABOUT QUANTILES - weekly')
print(' - Q1: ', round(np.quantile(inflation_list_1,0.25) * 100, 3), '%')
print(' - Q3: ', round(np.quantile(inflation_list_1,0.75) * 100, 3), '%')
print('')

a = input('Do you wanna see the graphs and charts (yes/no): ')
if a == 'yes':
    print('')
    print('-- Lets see the graphs')
    print('')

    a0 = input('Overall chart (yes/no): ')
    if a0 == 'yes':
        # CREATE GRAPH

        plt.subplot(2,2,1)
        plt.plot(date_list, cs_list)
        plt.xlabel('Date')
        plt.ylabel('Circulation supply')
        plt.title('Token inflation')

        plt.subplot(2,2,2)
        plt.bar(number_list, inflation_list, width=0.8, color='black')
        plt.plot(number_list, avg_monthly_list)
        plt.xlabel('Number of months')
        plt.ylabel('Inflation per month')
        plt.title('Inflation per month for token')

        plt.subplot(2,2,3)
        plt.bar(number_list_1, inflation_list_1, width=0.8, color='black')
        plt.plot(number_list_1, avg_weekly_list)
        plt.xlabel('Number of weeks')
        plt.ylabel('Inflation per week')
        plt.title('Inflation per week for token')

        plt.subplot(2,2,4)
        plt.bar(number_list, sum_list, width=0.8, color='black')
        plt.xlabel('Number of months')
        plt.ylabel('Inflation per month')
        plt.title('Sum Inflation per month for token')

        plt.show()

    # DIFFERENT CHART

    a1 = input('Do you wanna see number of tokens inflated (yes/no): ')
    if a1 == 'yes':
        plt.subplot(2,2,1)
        plt.bar(number_list_1, new_tokens_7_list, color='black')
        plt.ylabel('Weekly : nº of new tokens in circ.')

        plt.subplot(2,2,2)
        plt.bar(number_list_1, value_new_tokens_7_list, color='black')
        plt.ylabel('Weekly : in $ new tokes in circ.')

        plt.subplot(2,2,3)
        plt.bar(number_list, new_tokens_30_list, color='black')
        plt.ylabel('Monthly : nº of new tokens in circ.')

        plt.subplot(2,2,4)
        plt.bar(number_list, value_new_tokens_30_list, color='black')
        plt.ylabel('Monthly : in $ new tokes in circ.')

        plt.show()

    a3 = input('Do you wanna see table with chart values (yes/no): ')
    a4 = input('Weekly or Monthly view (weekly/monthly): ')
    if a3 == 'yes':
        if a4 == 'weekly':
            head = [
                'Weekly',
                'Qt of new tokens',
                'New tokens in $'
            ]
            table = tuple(data_for_table_list)
            print(tabulate([[row[0], "{:,}".format(row[1]), "{:,}".format(row[2])] for row in table], headers=head, tablefmt='grid', floatfmt=".0f"))
        elif a4 == 'monthly':
            head = [
                'Monthly',
                'Qt of new tokens',
                'New tokens in $'
            ]
            table = tuple(data_for_table_list_monthly)
            print(tabulate([[row[0], "{:,}".format(row[1]), "{:,}".format(row[2])] for row in table], headers=head, tablefmt='grid', floatfmt=".0f"))


    a2 = input('Do you wanna see daily chart (yes/no): ')
    if a2 == 'yes':
        plt.bar(number_daily_list, daily_inflation_list, color='black')
        plt.plot(number_daily_list, avg_daily_list)
        plt.ylabel('Inflation % per Day')
        plt.title('Daily inflation for : ' + str(crypto))

        plt.show()

print('DONE --')