import sqlite3
from pprint import pprint
import statistics
import matplotlib.pyplot as plt

conn = sqlite3.connect('historical_prices.sqlite')
cur = conn.cursor()

symbol = input('Select symbol (ETHUSDT): ')
candle_time = input('SELECT the candle time (1m/5m/15m/1H/4H/1D/1M): ')

table = symbol + '_' + candle_time

cur.execute(
    '''SELECT close_price FROM {}'''.format(table)
)
info = cur.fetchall()

sma_list_20 = list()
sma_list_50 = list()
sma_list_100 = list()

sma_20 = list()
sma_50 = list()
sma_100 = list()

market_price = list()

number = 0
for n in info:
    number += 1

    price = n[0]
    if number > 99:
        market_price.append(price)

    if len(sma_list_20) < 20:
        sma_list_20.append(price)
    else:
        first_element = sma_list_20[0]
        sma_list_20.remove(first_element)
        sma_list_20.append(price)

    if len(sma_list_50) < 50:
        sma_list_50.append(price)
    else:
        first_element = sma_list_50[0]
        sma_list_50.remove(first_element)
        sma_list_50.append(price)

    if len(sma_list_100) < 100:
        sma_list_100.append(price)
    else:
        first_element = sma_list_100[0]
        sma_list_100.remove(first_element)
        sma_list_100.append(price)

    if len(sma_list_20) == 20 and number > 99:
        sma = statistics.mean(sma_list_20)
        sma_20.append(sma)

    if len(sma_list_50) == 50 and number > 99:
        sma = statistics.mean(sma_list_50)
        sma_50.append(sma)

    if len(sma_list_100) == 100 and number > 99:
        sma = statistics.mean(sma_list_100)
        sma_100.append(sma)

size_market_price = len(market_price)
size_sma_20 = len(sma_20)
size_sma_50 = len(sma_50)
size_sma_100 = len(sma_100)

ratio_list_100 = list()
ratio_list_50 = list()
ratio_list_100_percentage = list()

zeros = list()
half = list()
hundreds = list()
oneandhalf = list()
twohundreds = list()
halfnegative = list()
hundreds_negatives = list()
oneandhalfnegative = list()
twohundreds_negatives = list()

for i in range(len(market_price)):
    price_value = market_price[i]
    sma_20_value = sma_20[i]
    sma_50_value = sma_50[i]
    sma_100_value = sma_100[i]
    '''
    Create some edition to try new approach
    '''
    ratio_100 = float(price_value) - float(sma_100_value)
    ratio_list_100.append(ratio_100)

    ratio_100_percentage = (float(price_value) - float(sma_100_value))/float(price_value)
    ratio_list_100_percentage.append(ratio_100_percentage)

    ratio_50 = float(price_value) - float(sma_50_value)
    ratio_list_50.append(ratio_50)

    zeros.append(0)
    half.append(0.1)
    hundreds.append(0.2)
    oneandhalf.append(0.3)
    twohundreds.append(0.4)
    halfnegative.append(-0.1)
    hundreds_negatives.append(-0.2)
    oneandhalfnegative.append(-0.3)
    twohundreds_negatives.append(-0.4)


plt.subplot(3,1,1)
plt.title(table)
plt.plot(range(size_market_price), market_price)
plt.plot(range(size_sma_20), sma_20)
plt.plot(range(size_sma_50), sma_50)
plt.plot(range(size_sma_100), sma_100)

plt.subplot(3,1,2)
plt.plot(range(size_market_price), ratio_list_100, label='Market_price - SMA_100')
plt.plot(range(size_market_price), zeros)
# plt.plot(range(size_market_price), ratio_list_50, label='SMA_50')

# plt.plot(range(size_market_price), half)
# plt.plot(range(size_market_price), hundreds)
# plt.plot(range(size_market_price), oneandhalf)
# plt.plot(range(size_market_price), twohundreds)
# plt.plot(range(size_market_price), halfnegative)
# plt.plot(range(size_market_price), hundreds_negatives)
# plt.plot(range(size_market_price), oneandhalfnegative)
# plt.plot(range(size_market_price), twohundreds_negatives)

plt.subplot(3,1,3)
plt.plot(range(size_market_price), ratio_list_100_percentage, label='Market_price - SMA_100 %')

plt.plot(range(size_market_price), zeros)
plt.plot(range(size_market_price), half)
plt.plot(range(size_market_price), hundreds)
plt.plot(range(size_market_price), oneandhalf)
plt.plot(range(size_market_price), twohundreds)
plt.plot(range(size_market_price), halfnegative)
plt.plot(range(size_market_price), hundreds_negatives)
plt.plot(range(size_market_price), oneandhalfnegative)
plt.plot(range(size_market_price), twohundreds_negatives)

plt.legend()
plt.show()