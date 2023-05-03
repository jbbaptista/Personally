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
id_l = list()
marketcap_l = list()
data_for_table_l = list()
market_share_perc_l = list()
volume_24h_l = list()
volume_24h_perc_l = list()
perc_vol_marketcap_l = list()
market_cap_changes_24h_l = list()
n_l = list()
positive_marketcap_changes = list()
negative_marketcap_changes = list()
for i in range(len(response)):
    v = response[i]['name']
    id = response[i]['id']
    n = i + 1

    try:
        market_cap = round(float(response[i]['market_cap']), 3)
        market_cap_changes_24h = round(float(response[i]['market_cap_change_24h']), 3)
    except:
        market_cap = 0
        market_cap_changes_24h = 0
        continue
    perc = round(market_cap / total_marketcap * 100, 2)
    try:
        volume_24h = round(float(response[i]['volume_24h']), 3)
    except:
        volume_24h = 0
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
    id_l.append(id)
    market_cap_changes_24h_l.append(market_cap_changes_24h)
    n_l.append(n)
    if market_cap_changes_24h > 0:
        positive_marketcap_changes.append(market_cap_changes_24h)
    elif market_cap_changes_24h <0:
        negative_marketcap_changes.append(market_cap_changes_24h)

    # CALCULATIONS

    if market_cap / 1000000 < 1000:
        marketcap2 = str(round(market_cap / 1000000, 3)) + ' M'
    else:
        marketcap2 = str(round(market_cap/1000000000, 3)) + ' B'

    if volume_24h / 1000000 < 1000:
        volume_24h2 = str(round(volume_24h / 1000000, 3)) + ' M'
    else:
        volume_24h2 = str(round(volume_24h / 1000000000, 3)) + ' B'

    a = (n, v, id, marketcap2, perc, volume_24h2, perc_volume, perc_vol_marketcap, market_cap_changes_24h)
    data_for_table_l.append(a)

# PRINT MORE VALUES

avg_marketcap_perc = round(np.average(market_cap_changes_24h_l), 3)
print('Avg MCap 24h %: ', avg_marketcap_perc, '%')
positive_avg_marketcap_perc = round(np.average(positive_marketcap_changes), 3)
print('Positive sectors - Avg MCap 24h %: ', positive_avg_marketcap_perc, '%')
negative_avg_marketcap_perc = round(np.average(negative_marketcap_changes), 3)
print('Negative sectors - Avg MCap 24h %: ', negative_avg_marketcap_perc, '%')
print('')


# PRINT VALUES IN TABLE

a = input('You want to see the values in table (yes/no): ')
if a == 'yes':
    head = ['n',
            'Sector',
            'id',
            'MarketCap',
            'MCap-TotMCap %',
            'Volume 24h',
            'Vol-TotVol %',
            'Vol-MCap %',
            'MCap 24h %'
            ]
    print(tabulate(data_for_table_l, headers=head, tablefmt='grid'))

# q1 = input('Do you wanna order by the MCap 24h % (yes/no): ')
# if q1 == 'yes':
#     sorted_list = sorted(data_for_table_l, key=lambda x: x[8], reverse=True)
#     head = ['n',
#             'Sector',
#             'id',
#             'MarketCap',
#             'MCap-TotMCap %',
#             'Volume 24h',
#             'Vol-TotVol %',
#             'Vol-MCap %',
#             'MCap 24h %'
#             ]
#     print(tabulate(sorted_list, headers=head, tablefmt='grid'))
#
# # CREATE GRAPH TO GET ALL INFO
#
# print('')
# b1 = input('Graphs (yes/no): ')
# if b1 == 'yes':
#     b = input('Graph by market cap (yes/no): ')
#     if b == 'yes':
#         fig, (ax1, ax2) = plt.subplots(2, sharex=True)
#         fig.suptitle ('All crypto sectores')
#
#         ax1.bar(sector_l, marketcap_l)
#         ax2.bar(sector_l, marketcap_l)
#
#         plt.yscale('log')
#         plt.xticks(fontsize=8, rotation='vertical')
#         plt.ylabel('MarketCap')
#
#
#         plt.tight_layout()
#         plt.subplots_adjust(hspace=0.05)
#         plt.show()
#
#     c = input('Graph Market share (yes/no): ')
#     if c =='yes':
#         plt.bar(sector_l, market_share_perc_l)
#         plt.title('Market share by sectores')
#         plt.ylabel('%')
#         plt.xticks(fontsize=8, rotation='vertical')
#
#         plt.tight_layout()
#         plt.show()
#
#     d = input('Graph for MarketCap and Volume (yes/no): ')
#     if d == 'yes':
#         fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
#         fig.suptitle('Info for all sectores')
#
#         size = np.arange(len(sector_l))
#
#         bar1 = ax1.bar(size, marketcap_l, 0.35, label='MarketCap')
#         bar2 = ax1.bar(size + 0.25, volume_24h_l, 0.35,  label='Volume 24h')
#
#         ax1.legend((bar1, bar2), ('MarketCap', 'Volume 24h'))
#
#         bar3 = ax2.bar(size, market_share_perc_l, 0.35, label = 'Market share %')
#         bar4 = ax2.bar(size + 0.5, volume_24h_perc_l, 0.35, label='Vol/Total Volume %')
#         bar5 = ax2.bar(size + 0.25, perc_vol_marketcap_l, 0.35, label = 'Vol/MarketCap %')
#
#         ax2.legend((bar3, bar4, bar5), ('Market share %', 'Vol/Total Volume %', 'Vol/MarketCap %'))
#
#         bar6 = ax3.bar(size, market_share_perc_l, 0.35, label = 'Market share %')
#         bar7 = ax3.bar(size + 0.5, volume_24h_perc_l, 0.35, label='Vol/Total Volume %')
#         bar8 = ax3.bar(size + 0.25, perc_vol_marketcap_l, 0.35, label = 'Vol/MarketCap %')
#
#         ax3.legend((bar6, bar7, bar8), ('Market share %', 'Vol/Total Volume %', 'Vol/MarketCap %'), prop={'size':6})
#
#         plt.yscale('log')
#
#         plt.xticks(size + 0.25, sector_l, fontsize=8, rotation='vertical')
#         plt.subplots_adjust(hspace=0.05)
#         plt.show()

print('\n-- DATABASE INFORMATION \n')
import sqlite3

# Create a connection to the SQLite database and create a cursor object
conn = sqlite3.connect("crypto_data.db")
cursor = conn.cursor()

# Get the current date
import datetime
current_date = datetime.datetime.now().strftime("%Y_%m_%d")

# Function to check if a column exists in a table
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    return column_name in columns


# Create market_cap table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS market_cap (
    sector_id TEXT PRIMARY KEY,
    sector_name TEXT
)
""")
print("Created market_cap table if not exists")

# Create daily_volume table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_volume (
    sector_id TEXT PRIMARY KEY,
    sector_name TEXT
)
""")
print("Created daily_volume table if not exists")

# Add a prefix to the current_date to avoid column names starting with a number
current_date_column = f"date_{current_date}"

# Add a column for the current date if it doesn't exist
if not column_exists(cursor, "market_cap", current_date_column):
    cursor.execute(f"ALTER TABLE market_cap ADD COLUMN {current_date_column} REAL")
    print(f"Added column {current_date_column} to market_cap table")

if not column_exists(cursor, "daily_volume", current_date_column):
    cursor.execute(f"ALTER TABLE daily_volume ADD COLUMN {current_date_column} REAL")
    print(f"Added column {current_date_column} to daily_volume table")

# Update market cap and daily volume information for each sector
for i in range(len(response)):
    sector_id = response[i]['id']
    sector_name = response[i]['name']

    try:
        market_cap = round(float(response[i]['market_cap']), 3)
    except:
        market_cap = None

    try:
        volume_24h = round(float(response[i]['volume_24h']), 3)
    except:
        volume_24h = None

    print(f"Processing sector: {sector_name}")

    # Insert or update the sector in the market_cap table
    cursor.execute("""
    INSERT OR IGNORE INTO market_cap (sector_id, sector_name)
    VALUES (?, ?)
    """, (sector_id, sector_name))
    if market_cap is not None:
        cursor.execute(f"""
        UPDATE market_cap
        SET {current_date_column} = ?
        WHERE sector_id = ?
        """, (market_cap, sector_id))
        print(f"Updated market cap for {sector_name} on {current_date}")

    # Insert or update the sector in the daily_volume table
    cursor.execute("""
    INSERT OR IGNORE INTO daily_volume (sector_id, sector_name)
    VALUES (?, ?)
    """, (sector_id, sector_name))
    if volume_24h is not None:
        cursor.execute(f"""
        UPDATE daily_volume
        SET {current_date_column} = ?
        WHERE sector_id = ?
        """, (volume_24h, sector_id))
        print(f"Updated daily volume for {sector_name} on {current_date}")

# Commit the changes and close the connection
conn.commit()
conn.close()
print("\n Changes committed and connection closed")




