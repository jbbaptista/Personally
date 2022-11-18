import datetime
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''

GOAL IS TO CLEAN THE DATA
CLEAN THE OUTLIERS TO CLEAR STATISTIC VALUES

'''

# CHOOSE THE TABLES TO CLEAN

print('')
table1 = input('Choose the table 1: ')
table2 = input('Choose the table 2: ')
print('')

# CONNECTION WITH DATA

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

# GET THE DATA

cur.execute('''
SELECT date, price_var
FROM {} '''.format(table1)
            )
data1 = cur.fetchall()

cur.execute('''
SELECT date, price_var
FROM {} '''.format(table2)
            )
data2 = cur.fetchall()

values1 = list()
for i in range(len(data1)):
    a = data1[i][1]
    values1.append(a)

values2 = list()
for i in range(len(data2)):
    a = data2[i][1]
    values2.append(a)

# READ THE DATA

    # GET THE INTERQUARTILE VALUES

q1_1 = np.percentile(values1, 25)
q2_1 = np.percentile(values1, 50)
q3_1 = np.percentile(values1, 75)

iqr_1 = float(q3_1) - float(q1_1)
h_1 = q3_1 + 3 * iqr_1
l_1 = q1_1 - 3 * iqr_1

print('-- GET QUARTILE VALUES --')
print('')
print('-- FOR TABLE 1')
print('')
print('Quartile 1: ', q1_1)
print('Quartile 2: ', q2_1)
print('Quartile 3: ', q3_1)
print('')
print('IQR: ', iqr_1)
print('')
print('Higher value: ', h_1)
print('Lower value: ', l_1)
print('')

q1_2 = np.percentile(values2, 25)
q2_2 = np.percentile(values2, 50)
q3_2 = np.percentile(values2, 75)

iqr_2 = float(q3_2) - float(q1_2)
h_2 = q3_2 + 3 * iqr_2
l_2 = q1_2 - 3 * iqr_2

print('-- FOR TABLE 2')
print('')
print('Quartile 1: ', q1_2)
print('Quartile 2: ', q2_2)
print('Quartile 3: ', q3_2)
print('')
print('IQR: ', iqr_2)
print('')
print('Higher value: ', h_2)
print('Lower value: ', l_2)
print('')

    # IDENTIFY OUTLIERS

print('-- START LOOPING TO INDENTIFY OUTLIERS --')
print('')
a = input('Do you want to clean the data (yes/no): ')
if a =='yes':
    print('-- TABLE 1')
    for i in range(len(data1)):
        a = float(data1[i][1])

        if a > h_1 or a < l_1:
            # print('OUTLIER IN i: ', i, ' // Value: ', a)

            # CLEAN DATA

            cur.execute(
                '''DELETE FROM {} 
                WHERE price_var = ? '''.format(table1) , (a, )
            )
            conn.commit()
            # print('DATA CLEAN IN DATE: ', data1[i][0], ' // Value: ', a)

    print('TABLE 1 -- CLEANING DONE')
    print('-- TABLE 2')
    for i in range(len(data2)):
        a = float(data2[i][1])

        if a > h_2 or a < l_2:
            # print('OUTLIER IN i: ', i, ' // Value: ', a)

            # CLEAN DATA

            cur.execute(
                '''DELETE FROM {} 
                WHERE price_var = ? '''.format(table2), (a,)
            )
            conn.commit()
            #print('DATA CLEAN IN DATE: ', data2[i][0], ' // Value: ', a)

    print('TABLE 2 -- CLEANING DONE')
    print('')
    
print('-- ITS COMPLETE --')




