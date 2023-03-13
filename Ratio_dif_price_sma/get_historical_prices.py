from binance.client import Client
import datetime
import pprint
import sqlite3
import accounts

SecretKey = accounts.SecretKey
APIKey = accounts.APIKey

client = Client(APIKey, SecretKey, {"timeout": 40})

symbol = input('Choose your crypto (BTCUSDT): ')
candle_time = input('Choose your candle time (1m/5m/15m/1H/4H/1D/1M): ')

conn = sqlite3.connect('historical_prices.sqlite')
cur = conn.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS {} (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    start_time TEXT, 
    open_price FLOAT, 
    close_price FLOAT, 
    low_price FLOAT, 
    high_price FLOAT,
    volume FLOAT,
    number_of_trades FLOAT)'''.format(symbol + '_' + candle_time)
)
conn.commit()

cur.execute(
    '''SELECT id, start_time, open_price, close_price, low_price, high_price, volume, number_of_trades 
    FROM {}'''.format(symbol + '_' + candle_time)
)
info = cur.fetchall()
last_number = len(info) - 1

if len(info) > 2:
    atual_time = datetime.datetime.now()
    last_time_database = datetime.datetime.fromisoformat(info[last_number][1])
    dif_time = atual_time - last_time_database

    hour = int(str(dif_time).split(':')[0])
    minute = int(str(dif_time).split(':')[1])

    number_of_candles = hour * 60 + minute
    if number_of_candles > 1500:
        number_of_candles = 1500
else:
    number_of_candles = 1500


'''
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
'''

if candle_time == '1m':
    info = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=number_of_candles)
if candle_time == '5m':
    info = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=1500)
if candle_time == '15m':
    info = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=1500)
if candle_time == '1H':
    info = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=1500)
if candle_time == '4H':
    info = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_4HOUR, limit=1500)
if candle_time == '1D':
    info = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=1500)
if candle_time == '1M':
    info = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MONTH, limit=1500)

for n in range(len(info)):
    time_string = info[n][0]
    start_time = datetime.datetime.fromtimestamp(time_string / 1000)
    open_price = info[n][1]
    close_price = info[n][4]
    low_price = info[n][3]
    high_price = info[n][2]
    volume = info[n][5]
    number_of_trades = info[n][8]

    cur.execute(
        '''INSERT INTO {} (start_time, open_price, close_price, low_price, high_price, volume, number_of_trades)
        VALUES (?,?,?,?,?,?,?)'''.format(symbol + '_' + candle_time), (start_time, open_price, close_price, low_price, high_price, volume, number_of_trades)
    )
    conn.commit()

conn.close()
print('--Its completed--')