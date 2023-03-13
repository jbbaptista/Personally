import requests
import pprint
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np


print('')
print('- GLOBAL INFO -')
print('')

# CONNECT WITH THE API

url = 'https://api.coingecko.com/api/v3/coins/categories'

r = requests.get(url)
response = r.json()

# pprint.pprint(response)
# exit()

# GET TOTAL MARKET CAP

url1 = 'https://api.coingecko.com/api/v3/global'

r1 = requests.get(url1)
response1 = r1.json()

total_marketcap = round(response1['data']['total_market_cap']['usd'], 3)
total_volume = round(response1['data']['total_volume']['usd'], 3)
print('Total Crypto MarketCap: {0:12,.3f}'.format(total_marketcap))
print('Total Crypto 24h Volume: {0:12,.3f}'.format(total_volume))

bb = round(total_volume / total_marketcap * 100, 2)
print('Total Volume 24h / Total MarketCap (%): ', bb ,'%')

print('')
# GET THE NAME OF THE SECTORES

sector_l = list()
marketcap_l = list()
data_for_table_l = list()
market_share_perc_l = list()
volume_24h_l = list()
volume_24h_perc_l = list()
perc_vol_marketcap_l = list()
for i in range(len(response)):
    v = response[i]['name']
    market_cap = round(float(response[i]['market_cap']), 3)
    perc = round(market_cap / total_marketcap * 100, 2)
    volume_24h = round(float(response[i]['volume_24h']),3)
    perc_volume = round(volume_24h / total_volume * 100, 2)
    if market_cap != 0:
        perc_vol_marketcap = round(volume_24h / market_cap * 100, 2)
    else:
        perc_vol_marketcap = 0

    # INSERT INTO LISTS

    sector_l.append(v)
    marketcap_l.append(market_cap)
    market_share_perc_l.append(perc)
    volume_24h_l.append(volume_24h)
    volume_24h_perc_l.append(perc_volume)
    perc_vol_marketcap_l.append(perc_vol_marketcap)

    # CALCULATIONS

    if market_cap / 1000000 < 1000:
        marketcap2 = str(round(market_cap / 1000000, 3)) + ' M'
    else:
        marketcap2 = str(round(market_cap/1000000000, 3)) + ' B'

    if volume_24h / 1000000 < 1000:
        volume_24h2 = str(round(volume_24h / 1000000, 3)) + ' M'
    else:
        volume_24h2 = str(round(volume_24h / 1000000000, 3)) + ' B'

    a = (v, marketcap2, perc, volume_24h2, perc_volume, perc_vol_marketcap)
    data_for_table_l.append(a)

# PRINT VALUES IN TABLE

a = input('You want to see the values in table (yes/no): ')
if a == 'yes':
    head = ['Sector',
            'MarketCap',
            'MCap-TotMCap %',
            'Volume 24h',
            'Vol-TotVol %',
            'Vol-MCap %']
    print(tabulate(data_for_table_l, headers=head, tablefmt='grid'))

# CREATE GRAPH TO GET ALL INFO

print('')
b1 = input('Graphs (yes/no): ')
if b1 == 'yes':
    b = input('Graph by market cap (yes/no): ')
    if b == 'yes':
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        fig.suptitle ('All crypto sectores')

        ax1.bar(sector_l, marketcap_l)
        ax2.bar(sector_l, marketcap_l)

        plt.yscale('log')
        plt.xticks(fontsize=8, rotation='vertical')
        plt.ylabel('MarketCap')


        plt.tight_layout()
        plt.subplots_adjust(hspace=0.05)
        plt.show()

    c = input('Graph Market share (yes/no): ')
    if c =='yes':
        plt.bar(sector_l, market_share_perc_l)
        plt.title('Market share by sectores')
        plt.ylabel('%')
        plt.xticks(fontsize=8, rotation='vertical')

        plt.tight_layout()
        plt.show()

    d = input('Graph for MarketCap and Volume (yes/no): ')
    if d == 'yes':
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
        fig.suptitle('Info for all sectores')

        size = np.arange(len(sector_l))

        bar1 = ax1.bar(size, marketcap_l, 0.35, label='MarketCap')
        bar2 = ax1.bar(size + 0.25, volume_24h_l, 0.35,  label='Volume 24h')

        ax1.legend((bar1, bar2), ('MarketCap', 'Volume 24h'))

        bar3 = ax2.bar(size, market_share_perc_l, 0.35, label = 'Market share %')
        bar4 = ax2.bar(size + 0.5, volume_24h_perc_l, 0.35, label='Vol/Total Volume %')
        bar5 = ax2.bar(size + 0.25, perc_vol_marketcap_l, 0.35, label = 'Vol/MarketCap %')

        ax2.legend((bar3, bar4, bar5), ('Market share %', 'Vol/Total Volume %', 'Vol/MarketCap %'))

        bar6 = ax3.bar(size, market_share_perc_l, 0.35, label = 'Market share %')
        bar7 = ax3.bar(size + 0.5, volume_24h_perc_l, 0.35, label='Vol/Total Volume %')
        bar8 = ax3.bar(size + 0.25, perc_vol_marketcap_l, 0.35, label = 'Vol/MarketCap %')

        ax3.legend((bar6, bar7, bar8), ('Market share %', 'Vol/Total Volume %', 'Vol/MarketCap %'), prop={'size':6})

        plt.yscale('log')

        plt.xticks(size + 0.25, sector_l, fontsize=8, rotation='vertical')
        plt.subplots_adjust(hspace=0.05)
        plt.show()
