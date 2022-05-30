import sqlite3
import pprint
from matplotlib import pyplot

print('--START TEST--')

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

table_name = input('Choose the name of table: ')

cur.execute(
    '''SELECT open, high, low, close 
    FROM {}'''.format(table_name)
)
info = cur.fetchall()

pprint.pprint(info)

close = list()
open = list()
for i in range(len(info)):
    v1 = float(info[i][3])
    close.append(v1)

    v2 = float(info[i][0])
    open.append(v1)

pyplot.boxplot(info)
pyplot.show()

