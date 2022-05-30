import sqlite3
from matplotlib import pyplot

print('--START THE NEW CHART--')

# Comunication with database

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

# Choose the pair

pair = input('Please choose the pair (ETHUSDT): ')

# Take all info out

pair_60m = pair + '_60m'
cur.execute(
    '''SELECT time, open, high, low, close, volume
    FROM {}'''.format(pair_60m)
)
info_60m = cur.fetchall()

pair_1D = pair + '_1D'
cur.execute(
    '''SELECT time, open, high, low, close, volume
    FROM {}'''.format(pair_1D)
)
info_1D = cur.fetchall()

# See the star time when the small time have data

start_time = str(info_60m[0][0]).split(' ')[0]
print(start_time)
start_day = str(start_time).split(' ')[0].split('-')[2]
start_month = str(start_time).split(' ')[0].split('-')[1]
start_year = str(start_time).split(' ')[0].split('-')[0]
print(start_day, start_month, start_year)

    # See what is the line to start on the higher timelime

start_line = None
for i in range(len(info_1D)):
    time = str(info_1D[i][0]).split(' ')[0]

    if time == start_time:
        start_line = i
        print('Start line =', start_line)
        break

# Time to see values in higher timeframe

'''

Definition of ranges to analyse the inert volume 

range_1 -> range [higher 1, higher 2]
range_2 -> range [higher 2, avg (open,close)]
range_3 -> range [avg (open, close), higher 3]
range_4 -> range [higher 3, higher 4]

'''

agg = list()
for i in range(start_line, len(info_1D)):
    time = str(info_1D[i][0]).split(' ')[0]
    open = float(info_1D[i][1])
    high = float(info_1D[i][2])
    low = float(info_1D[i][3])
    close = float(info_1D[i][4])
    avg = (open + close) / 2

    print(time, open, high, low, close)
    a = (open, high, low, close)
    agg.append(a)

print(agg)
pyplot.boxplot(agg)
pyplot.show()


