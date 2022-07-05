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

print('')
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

if len(info1) > len(info2):
    size = len(info1)
else:
    size = len(info2)

data1 = list()
data2 = list()

# CLEAN LAST VALUES FOR CORRELATION TABLE

cur.execute('''
DROP TABLE IF EXISTS corr''')

# START LOOP

print('')
print('-- STARTING LOOP FOR CORRELATION --')
for i in range(len(info1)):
    time1 = info1[i][0]
    get_v_1 = info1[i][1]

    for i in range(len(info2)):
        time2 = info2[i][0]
        get_v_2 = info2[i][1]

        if time1 == time2:
            # python3print('-- SAME DATE -- in i: ', i, ' // Time: ', time1, time2, ' // v: ', get_v_1, get_v_2)

            # INSERT IN LIST

            data1.append(get_v_1)
            data2.append(get_v_2)

            # CREATE NEW TABLE WITH 2 ASSETS
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS corr (
                date TEXT,
                {} FLOAT,
                {} FLOAT)'''.format(table1, table2)
            )
            cur.execute(
                '''INSERT INTO corr (date, {}, {})
                VALUES (?,?,?)'''.format(table1,table2), (time1, float(get_v_1), float(get_v_2))
            )
            conn.commit()

print('DONE --')
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
print('')
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

q = input('Show the graphs (yes/no): ')
print('')

if q == 'yes':
    sns.pairplot(db, kind='scatter')
    pyplot.show()

    sns.lmplot(data=db, x=table1, y=table2)
    pyplot.show()

    sns.displot(data=db, kde=True)
    pyplot.show()

# MANIPULATE THE DATA TO GET THE CORRELATION BY PERIODS OF TIMES

print('-- START CALCULATION BY PERIODS FOR CORRELATION--')

data1_30 = list()
data1_60 = list()
data1_90 = list()
data2_30 = list()
data2_60 = list()
data2_90 = list()
corr_p_30 = list()
corr_p_60 = list()
corr_p_90 = list()
corr_s_30 = list()
corr_s_60 = list()
corr_s_90 = list()
for i in range(len(data1)):

    v1 = data1[i]
    v2 = data2[i]

    # ADD VALUES TO THE LISTS

        # VALUES 1

    data1_30.append(v1)
    data1_60.append(v1)
    data1_90.append(v1)

        # VALUES 2

    data2_30.append(v2)
    data2_60.append(v2)
    data2_90.append(v2)

    # DELETE THE FIRST VALUE OF THE LIST

    if i > 30 - 1:
        data1_30.remove(data1_30[0])
        data2_30.remove(data2_30[0])

        # GET CORRELATION VALUES

            # Pearson model
        corr1, _ = pearsonr(data1_30, data2_30)
        # print('Pearsons correlation: %.3f' % corr1)
        corr_p_30.append(corr1)

            # Spearman model
        corr2, _ = spearmanr(data1_30, data2_30)
        # print('Spearmans correlation: %.3f' % corr2)
        corr_s_30.append(corr2)

    if i > 60 - 1:
        data1_60.remove(data1_60[0])
        data2_60.remove(data2_60[0])

        # GET CORRELATION VALUES

            # Pearson model
        corr1, _ = pearsonr(data1_60, data2_60)
        # print('Pearsons correlation: %.3f' % corr1)
        corr_p_60.append(corr1)

            # Spearman model
        corr2, _ = spearmanr(data1_60, data2_60)
        # print('Spearmans correlation: %.3f' % corr2)
        corr_s_60.append(corr2)

    if i > 90 - 1:
        data1_90.remove(data1_90[0])
        data2_90.remove(data2_90[0])

        # GET CORRELATION VALUES

            # Pearson model
        corr1, _ = pearsonr(data1_90, data2_90)
        # print('Pearsons correlation: %.3f' % corr1)
        corr_p_90.append(corr1)

            # Spearman model
        corr2, _ = spearmanr(data1_90, data2_90)
        # print('Spearmans correlation: %.3f' % corr2)
        corr_s_90.append(corr2)

print('DONE --')
print('')

# GET CHARTS FOR CORRELATION VALUE

t = input('Charts for correlation by period (yes/no): ')
print('')

if t == 'yes':
    print('PEARSON R VALUES --')
    pyplot.plot(corr_p_30)
    pyplot.plot(corr_p_60)
    pyplot.plot(corr_p_90)
    pyplot.ylabel('Correlation Pearson values')
    pyplot.legend(['corr w/ 30', 'corr w/ 60', 'corr w/ 90'], loc = 'lower right')
    pyplot.show()

    print('SPEARMANS VALUES --')
    pyplot.plot(corr_s_30)
    pyplot.plot(corr_s_60)
    pyplot.plot(corr_s_90)
    pyplot.ylabel('Correlation Spearmans values')
    pyplot.legend(['corr w/ 30', 'corr w/ 60', 'corr w/ 90'], loc = 'lower right')
    pyplot.show()







print('-- ITS COMPLETE --')



