import sqlite3
import numpy
from matplotlib import pyplot
from scipy.stats import pearsonr, spearmanr
import seaborn as sns
import pandas as pd

'''

HERE WE READ THE DATABASE 
AND GET STATISTICAL VALUES / GRAPH'S ABOUT CORRELATION


'''

# Connect to database
conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

# Choose the tables

table1 = input('Insert name of table1: ')
table2 = input('Insert name of table2: ')

# Take values from database

cur.execute(
    '''SELECT date, price_var 
    FROM {}'''.format(table1)
)
info1 = cur.fetchall()

cur.execute(
    '''SELECT date, price_var
    FROM {}'''.format(table2)
)
info2 = cur.fetchall()

if len(info1) < len(info2):
    size = len(info1)
else:
    size = len(info2)

data1 = list()
data2 = list()

# CLEAN LAST VALUES FOR CORRELATION TABLE

cur.execute('''
DROP TABLE IF EXISTS corr''')

# START LOOP
for i in range(1, size):
    time1 = info1[-i][0]
    time2 = info2[-i][0]

    if time1 != time2:
        print('--Different-- in i: ', i)

    insert1 = info1[-i][1]
    data1.append(insert1)

    insert2 = info2[-i][1]
    data2.append(insert2)

    # CREATE NEW TABLE WITH 2 ASSETS
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS corr (
        date TEXT,
        {} FLOAT,
        {} FLOAT)'''.format(table1, table2)
    )
    cur.execute(
        '''INSERT INTO corr (date, {}, {})
        VALUES (?,?,?)'''.format(table1,table2), (time1, float(insert1), float(insert2))
    )
    conn.commit()

# Make some statistics

if min(data1) < min(data2):
    minv = int(min(data1))
else:
    minv = int(min(data2))

if max(data1) > max(data2):
    maxv = int(max(data1))
else:
    maxv = int(max(data2))

# pyplot.scatter(data1,data2)
# z = numpy.polyfit(data1,data2,1)
# p = numpy.poly1d(z)
# pyplot.plot(data1,p(data1))
# pyplot.plot(range(minv,maxv),range(minv,maxv))
# pyplot.show()

print('')
print('-- STATISTICS VALUES --')
covariance = numpy.cov(data1, data2)
print('Covariance: ', covariance)

# Pearson model
corr1, _ = pearsonr(data1,data2)
print('Pearsons correlation: %.3f' % corr1)

# Spearman model
corr2, _ = spearmanr(data1, data2)
print('Spearmans correlation: %.3f' % corr2)

# USE SEABORN

db = pd.read_sql_query('''
SELECT date, {}, {}
FROM corr'''.format(table1, table2), conn)

conn.close()
print('')

sns.pairplot(db, kind='scatter')
pyplot.show()

sns.lmplot(data=db, x=table1, y=table2)
pyplot.show()

sns.displot(data=db, kde=True)
pyplot.show()

print('-- ITS COMPLETE --')

