import sqlite3
import numpy
from matplotlib import pyplot
from scipy.stats import pearsonr, spearmanr

# Connect to database
conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

# Choose the tables

table1 = input('Insert name of table1: ')
table2 = input('Insert name of table2: ')

# Take values from database

cur.execute(
    '''SELECT time, var 
    FROM {}'''.format(table1)
)
info1 = cur.fetchall()

cur.execute(
    '''SELECT time, var
    FROM {}'''.format(table2)
)
info2 = cur.fetchall()

if len(info1) < len(info2):
    size = len(info1)
else:
    size = len(info2)

data1 = list()
data2 = list()
for i in range(1, size):
    time1 = info1[-i][0]
    time2 = info2[-i][0]

    if time1 != time2:
        print('--Different-- in i: ', i)

    insert1 = info1[-i][1]
    data1.append(insert1)

    insert2 = info2[-i][1]
    data2.append(insert2)

# Make some statistics

if min(data1) < min(data2):
    minv = int(min(data1))
else:
    minv = int(min(data2))

if max(data1) > max(data2):
    maxv = int(max(data1))
else:
    maxv = int(max(data2))

pyplot.scatter(data1,data2)
z = numpy.polyfit(data1,data2,1)
p = numpy.poly1d(z)
pyplot.plot(data1,p(data1))
pyplot.plot(range(minv,maxv),range(minv,maxv))
pyplot.show()

covariance = numpy.cov(data1, data2)
print('Covariance: ', covariance)

# Pearson model
corr1, _ = pearsonr(data1,data2)
print('Pearsons correlation: %.3f' % corr1)

# Spearman model
corr2, _ = spearmanr(data1, data2)
print('Spearmans correlation: %.3f' % corr2)

