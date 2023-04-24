import requests
import datetime
import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

'''

OBJETIVO E TIRAR O VOLUME E MARKET CAP DO COINGECKO 
-> RATIO RELACAO COM MARKET CAP
+ RATIOS E METRICAS - VALUES

'''

print('')
print('Important note -> Dont forget the name of the crypto is the API ID in coingecko')
print('')

# CHOOSE THE CRYPTO

crypto = input('Choose the crypto: ')
interval = input('Pick the timeline (weekly/daily): ')
n_days = input('Pick the number of values to look at (number/max): ')
if interval == 'daily':
    sma_input = 14
if interval == 'weekly':
    sma_input = 4

# GET ALL DATA

headers = {
    'id' : crypto,
    'vs_currency' : 'usd',
    'days' : n_days,
    'interval' : interval
}

url = 'https://api.coingecko.com/api/v3/coins/' + headers['id'] + '/market_chart?' + 'vs_currency=' + headers['vs_currency'] +'&days=' + headers['days'] + '&interval=' + headers['interval']

r = requests.get(url)
response = r.json()

# Test if we have the MarketCap available

url1 = f'https://api.coingecko.com/api/v3/coins/{crypto}'
r1 = requests.get(url1)
response1 = r1.json()

market_cap_test = response1['market_data']['market_cap']['usd']
fdv_validator = False
if market_cap_test == None or market_cap_test == 0:
    print('\nWe dont have the marketcap value available \n-- Working with FDV \n')
    fdv_validator = True
    total_supply = response1['market_data']['total_supply']

# IF SOMETHING GO WRONG

size = len(response)
if size < 3:
    print('')
    print('Probably the id is wrong')
    print('Open this link to find the correct id: https://api.coingecko.com/api/v3/coins/list')
    print('')
    exit()

# LOOP STARTS TO GET SOME PRECIOUS DATA

# WORK FIRST THE MARKET CAP


date_market_cap_l = list()
market_cap_l = list()
for i in range(len(response['market_caps'])):

    # GET THE VALUES

    date_v = response['market_caps'][i][0]
    if fdv_validator == False:
        market_cap_v = response['market_caps'][i][1]
    elif fdv_validator == True:
        market_cap_v = float(total_supply) * float(response['prices'][i][1])

    # PROTECTION

    if date_v == None or market_cap_v == 0 or market_cap_v == None:
        continue

    # WORK THE VALUES

    date = str(datetime.datetime.fromtimestamp(date_v / 1000)).split(' ')[0]
    market_cap = round(float(market_cap_v), 2)


    # ADD TO LIST

    date_market_cap_l.append(date)
    market_cap_l.append(market_cap)

# WORK SECOND WITH VOLUME

date_volume_l = list()
volume_l = list()
for j in range(len(response['total_volumes'])):

    # GET VALUES

    date_v = response['total_volumes'][j][0]
    volume_v = response['total_volumes'][j][1]

    # PROTECTION

    if date_v == None or volume_v == None or volume_v == 0:
        continue

    # WORK THE VALUES

    date = str(datetime.datetime.fromtimestamp(date_v / 1000)).split(' ')[0]
    volume = round(float(volume_v), 2)

    # ADD TO LIST

    date_volume_l.append(date)
    volume_l.append(volume)

ratio_l = list()
date_ratio_l = list()
market_cap_l_2 = list()
volume_l_2 = list()
for i in range(len(market_cap_l)):

    for j in range(len(date_volume_l)):
        if date_volume_l[j] == date_market_cap_l[i]:

            # GET VALUES

            date = date_volume_l[j]
            market_cap = market_cap_l[i]
            volume = volume_l[j]

            # GET MORE VALUES

            ratio = round(float(volume) / float(market_cap), 3)

            # print(date, market_cap, volume, ratio)

            # ADD TO LIST

            ratio_l.append(ratio)
            date_ratio_l.append(date)
            market_cap_l_2.append(market_cap)
            volume_l_2.append(volume)

# GET SMA

avg_l = list()
n = -1
sum = 0
for i in range(len(ratio_l)):
    sum = sum + ratio_l[i]
    if i > sma_input - 1:
        n += 1

        # GET VALUES

        avg = sum / sma_input

        # INSERT VALUES

        avg_l.append(avg)

        # CLEAN VALUES
        sum = sum - ratio_l[n]

    else:
        avg_l.append(0)

# GET SOME VALUES

print('')
print('-- INFO ABOUT VOLUME/MARKETCAP RATIO --')
print('')

actual_ratio = ratio_l[-1]
print('Actual Volume/MarketCap ratio: ', actual_ratio)
ath_ratio = max(ratio_l)
print('ATH Volume/MarketCap ratio: ', ath_ratio)
min1 = 100
for i in ratio_l:
    if float(i) == 0:
        continue
    elif float(i) < min1:
        min1 = float(i)
print('ATL Volume/MarketCap ratio: ', min1)
print('Last value for Volume/MarketCap ratio (avg): ', round(avg_l[-1], 3))

# ANALISE DE QUARTIS

print('')
print('-- Quartiles values')
print('')

q1 = round(np.quantile(ratio_l, 0.25), 3)
median = round(np.quantile(ratio_l, 0.5), 3)
q3 = round(np.quantile(ratio_l, 0.75), 3)
q0 = round(np.quantile(ratio_l, 0.10), 3)
q4 = round(np.quantile(ratio_l, 0.90), 3)

iqr = round(float(q3) - float(q1), 3)

print('Quartile 1: ', q1)
print('Median: ', median)
print('Quartile 3: ', q3)
print('')
print('IQR: ', iqr)
print('')
print('10% Distribution: ', q0)
print('90% Distribution: ', q4)

print('')
print('-- INFO ABOUT VOLUME --')
print('')

avg = round(np.average(volume_l), 3)
q1 = round(np.quantile(volume_l, 0.25), 3)
median = round(np.quantile(volume_l, 0.5), 3)
q3 = round(np.quantile(volume_l, 0.75), 3)
q0 = round(np.quantile(volume_l, 0.10), 3)
q4 = round(np.quantile(volume_l, 0.90), 3)

iqr = round(float(q3) - float(q1), 3)

print('Avg: {0:12,.3f}'.format(avg))
print('Quartile 1: {0:12,.3f}'.format(q1))
print('Median: {0:12,.3f}'.format(median))
print('Quartile 3: {0:12,.3f}'.format(q3))
print('')
print('IQR: {0:12,.3f}'.format(iqr))
print('')
print('10% Distribution: {0:12,.3f}'.format(q0))
print('90% Distribution: {0:12,.3f}'.format(q4))

# GET CHART

print('')
a = input('See charts (yes/no): ')
if a == 'yes':
    print('')
    print('- SHOW GRAPHS')
    print('')

    b1 = input('Do you wanna see the ratio charts (yes/no): ')
    if b1 == 'yes':
        plt.subplot(2,1,1)
        plt.plot(date_ratio_l, ratio_l)
        plt.plot(date_ratio_l, avg_l)
        # plt.plot(np.repeat(0.5,len(date_ratio_l)))
        # plt.plot(np.repeat(1,len(date_ratio_l)))
        plt.ylabel('Ratio: Volume / MarketCap')
        plt.title('Volume / MarketCap Indicator')

        plt.subplot(2,1,2)
        plt.plot(date_ratio_l, market_cap_l_2)
        plt.bar(date_ratio_l, volume_l_2)
        plt.xlabel('Date')
        plt.ylabel('MarketCap')

        plt.show()

        # OTHER GRAPHS

        sns.displot(data=ratio_l, kde=True)
        plt.title('Volume/MarketCap Distribution')
        plt.show()

        plt.boxplot(ratio_l)
        plt.title('Quartiles Distribution')
        plt.show()

    aa = input('Do you wanna see the volume chart alone (yes/no/yes with marketcap): ')
    if aa == 'yes':
        aa1 = input('Type of chart (log/linear): ')
        if aa1 == 'log':
            plt.bar(date_volume_l, volume_l)
            plt.yscale('log')
            plt.xlabel('Date')
            plt.ylabel('Volume')
            plt.title('Volume chart')
            plt.show()
        else:
            plt.bar(date_volume_l, volume_l)
            plt.xlabel('Date')
            plt.ylabel('Volume')
            plt.title('Volume chart')
            plt.show()

        sns.displot(data=volume_l, kde=True)
        plt.title('Volume Distribution')
        plt.show()

        plt.boxplot(volume_l)
        plt.title('Quartiles Distribution')
        plt.show()
    if aa == 'yes with marketcap':
        plt.subplot(2,1,1)
        plt.bar(date_volume_l, volume_l)
        plt.ylabel('Volume')

        plt.subplot(2,1,2)
        plt.plot(date_market_cap_l, market_cap_l)
        plt.xlabel('Date')
        plt.ylabel('MarketCap')

        plt.show()
    aaa = input('Do you wanna see the market cap chart alone (yes/no): ')
    if aaa == 'yes':
        aaa1 = input('Type of chart(log/linear): ')
        if aaa1 == 'log':
            plt.plot(date_market_cap_l, market_cap_l)
            plt.yscale('log')
            plt.xlabel('Date')
            plt.ylabel('MarketCap')
            plt.title('MarketCap chart')
            plt.show()
        else:
            plt.plot(date_market_cap_l, market_cap_l)
            plt.xlabel('Date')
            plt.ylabel('MarketCap')
            plt.title('MarketCap chart')
            plt.show()


print('')
print('DONE')



