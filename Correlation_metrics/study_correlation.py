import sqlite3
import numpy
from matplotlib import pyplot
from scipy.stats import pearsonr, spearmanr
import seaborn as sns
import pandas as pd
import pprint

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
a1 = input('Do you want to measure the beta value (yes/no): ')
if a1 == 'yes':
    market_table = input('what is the table as market_returns (data1/data2): ')

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
data_time = list()

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
            data_time.append(time1)
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

covariance = numpy.cov(data1, data2)[0][1]
print('Covariance: ', round(covariance,5))

if a1 == 'yes':
    if market_table == 'data1':
        variance = numpy.var(data1)
        print('Market variance: ', round(variance,5))
        print('')
    elif market_table == 'data2':
        variance = numpy.var(data2)
        print('Market variance: ', round(variance,5))
        print('')

    beta = covariance / variance
    print('Beta: ', round(beta,5))
    print('')

# Pearson model
corr1, _ = pearsonr(data1,data2)
print('Pearsons correlation: %.3f' % corr1)
print('p-value: ', pearsonr(data1,data2)[1])

# Spearman model
corr2, _ = spearmanr(data1, data2)
print('Spearmans correlation: %.3f' % corr2)
print('p-value: ', spearmanr(data1, data2)[1])

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
time_l = list()
beta_30_l = list()
stdev1_30_l = list()
stdev2_30_l = list()
x_l = list()
for i in range(len(data1)):

    v1 = data1[i]
    v2 = data2[i]
    time = data_time[i]

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
        corr1_30, _ = pearsonr(data1_30, data2_30)
        # print('Pearsons correlation: %.3f' % corr1)


            # Spearman model
        corr2_30, _ = spearmanr(data1_30, data2_30)
        # print('Spearmans correlation: %.3f' % corr2)

            # Beta value

        cov_30 = numpy.cov(data1_30, data2_30)[0][1]
        if market_table == 'data1':
            var_30 = numpy.var(data1_30)
        elif market_table == 'data2':
            var_30 = numpy.var(data2_30)

        beta_30 = round(cov_30 / var_30, 5)

        beta_30_l.append(beta_30)
        x_l.append(time)

            # Stdev

        stdev1_30 = numpy.std(data1_30)
        stdev2_30 = numpy.std(data2_30)

        stdev1_30_l.append(stdev1_30)
        stdev2_30_l.append(stdev2_30)

    if i > 60 - 1:
        data1_60.remove(data1_60[0])
        data2_60.remove(data2_60[0])

        # GET CORRELATION VALUES

            # Pearson model
        corr1_60, _ = pearsonr(data1_60, data2_60)
        # print('Pearsons correlation: %.3f' % corr1)

            # Spearman model
        corr2_60, _ = spearmanr(data1_60, data2_60)
        # print('Spearmans correlation: %.3f' % corr2)

    if i > 90 - 1:
        data1_90.remove(data1_90[0])
        data2_90.remove(data2_90[0])

        # GET CORRELATION VALUES

            # Pearson model
        corr1_90, _ = pearsonr(data1_90, data2_90)
        # print('Pearsons correlation: %.3f' % corr1)

            # Spearman model
        corr2_90, _ = spearmanr(data1_90, data2_90)
        # print('Spearmans correlation: %.3f' % corr2)

        # INSERT VALUES IN LIST

        corr_p_30.append(corr1_30)
        corr_s_30.append(corr2_30)
        corr_p_60.append(corr1_60)
        corr_s_60.append(corr2_60)
        corr_p_90.append(corr1_90)
        corr_s_90.append(corr2_90)

        time_l.append(time)

print('DONE --')
print('')

# GET CHARTS FOR CORRELATION VALUE

t = input('Charts for correlation by period (yes/no): ')
print('')

if t == 'yes':
    print('PEARSON R VALUES --')
    print('')
    print('Corr w/ 30 Values: ', round(corr_p_30[-1], 3))
    print('Corr w/ 60 Values: ', round(corr_p_60[-1], 3))
    print('Corr w/ 90 Values: ', round(corr_p_90[-1], 3))
    print('')
    a1 = input('Chart (yes/no): ')
    if a1 == 'yes':
        pyplot.plot(time_l, corr_p_30)
        pyplot.plot(time_l, corr_p_60)
        pyplot.plot(time_l, corr_p_90)
        pyplot.ylabel('Date')
        pyplot.ylabel('Correlation Pearson values')
        pyplot.legend(['corr w/ 30', 'corr w/ 60', 'corr w/ 90'], loc = 'lower right')
        pyplot.show()

    print('SPEARMANS VALUES --')
    print('')
    print('Corr w/ 30 Values: ', round(corr_s_30[-1], 3))
    print('Corr w/ 60 Values: ', round(corr_s_60[-1], 3))
    print('Corr w/ 90 Values: ', round(corr_s_90[-1], 3))
    print('')
    a2 = input('Chart (yes/no): ')
    if a2 == 'yes':
        pyplot.plot(time_l, corr_s_30)
        pyplot.plot(time_l, corr_s_60)
        pyplot.plot(time_l, corr_s_90)
        pyplot.xlabel('Date')
        pyplot.ylabel('Correlation Spearmans values')
        pyplot.legend(['corr w/ 30', 'corr w/ 60', 'corr w/ 90'], loc = 'lower right')
        pyplot.show()

a3 = input('Do you wanna see 30days beta chart (yes/no): ')
if a3 == 'yes':
    pyplot.plot(x_l, beta_30_l)
    pyplot.xlabel('Date')
    pyplot.title('Beta value - 30D values')
    pyplot.show()

a4 = input('Do you wanna see 30days stdev chart (yes/no): ')
if a4 == 'yes':
    pyplot.plot(x_l, stdev1_30_l, label='Stdev of ' + table1)
    pyplot.plot(x_l, stdev2_30_l, label='Stdev of ' + table2)
    pyplot.xlabel('Date')
    pyplot.title('Stdev values - 30D values')
    pyplot.legend(loc='lower right')
    pyplot.show()

print('')
print('-- ITS COMPLETE --')



