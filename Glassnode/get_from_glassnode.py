import requests
import pprint
import json
import datetime
from matplotlib import pyplot
import secret



'''
ALGO TO GET DATA FROM GLASSNODE
'''

print('')
print('Important note -> Dont forget the crypto needs to be on glassnode data')
print('')

# CHOOSE THE TOKEN

crypto = input('Choose the crypto name: ')

# GET DATA FROM GLASSNODE

api_key = secret.api_key

# TOTAL ADDRESSES

url = 'https://api.glassnode.com/v1/metrics/addresses/count'

r = requests.get(url,
                 params={
                     'a' : crypto,
                     'api_key' : api_key
                 })

response = r.json()

    # MANIPULATE DATA

total_addresses_l = list()
date_total_addresses_l = list()
sum = 0
avg_7_total_addresses_l = list()
for i in range(len(response)):
    date_value = response[i]['t']
    v = response[i]['v']
    sum += float(v)

    # WORK THE DATA

    date = str(datetime.datetime.fromtimestamp(date_value)).split(' ')[0]

    # AVG

    if i > 5:
        avg = sum / 7

        sum = sum - total_addresses_l[i-6]
    else:
        avg = 0

    # INSERT LIST

    total_addresses_l.append(v)
    date_total_addresses_l.append(date)
    avg_7_total_addresses_l.append(avg)

# ACTIVE ADDRESSES

url = 'https://api.glassnode.com/v1/metrics/addresses/active_count'

r = requests.get(url,
                 params={
                     'a' : crypto,
                     'api_key' : api_key
                 })

response = r.json()

# MANIPULATE DATA

active_addresses_l = list()
date_active_addresses_l = list()
sum = 0
avg_7_active_addresses = list()
for i in range(len(response)):
    date_value = response[i]['t']
    v = response[i]['v']
    sum += float(v)

    # WORK THE DATA

    date = str(datetime.datetime.fromtimestamp(date_value)).split(' ')[0]

    # AVG

    if i > 5:
        avg = sum / 7

        sum = sum - active_addresses_l[i - 6]
    else:
        avg = 0

    # INSERT LIST

    active_addresses_l.append(v)
    date_active_addresses_l.append(date)
    avg_7_active_addresses.append(avg)

# NEW ADDRESSES

url = 'https://api.glassnode.com/v1/metrics/addresses/new_non_zero_count'

r = requests.get(url,
                 params={
                     'a' : crypto,
                     'api_key' : api_key
                 })

response = r.json()

# MANIPULATE DATA

new_addresses_l = list()
date_new_addresses_l = list()
sum = 0
avg_7_new_addresses_l = list()
for i in range(len(response)):
    date_value = response[i]['t']
    v = response[i]['v']
    sum += float(v)

    # WORK THE DATA

    date = str(datetime.datetime.fromtimestamp(date_value)).split(' ')[0]

    # AVG

    if i > 5:
        avg = sum / 7

        sum = sum - new_addresses_l[i - 6]
    else:
        avg = 0

    # INSERT LIST

    new_addresses_l.append(v)
    date_new_addresses_l.append(date)
    avg_7_new_addresses_l.append(avg)

# NON-ZERO ADDRESSES

url = 'https://api.glassnode.com/v1/metrics/addresses/non_zero_count'

r = requests.get(url,
                 params={
                     'a' : crypto,
                     'api_key' : api_key
                 })

response = r.json()

# MANIPULATE DATA

non_zero_addresses_l = list()
date_non_zero_addresses_l = list()
sum = 0
avg_7_non_zero_addresses = list()
for i in range(len(response)):
    date_value = response[i]['t']
    v = response[i]['v']
    sum += float(v)

    # WORK THE DATA

    date = str(datetime.datetime.fromtimestamp(date_value)).split(' ')[0]

    # AVG

    if i > 5:
        avg = sum / 7

        sum = sum - non_zero_addresses_l[i - 6]
    else:
        avg = 0

    # INSERT LIST

    non_zero_addresses_l.append(v)
    date_non_zero_addresses_l.append(date)
    avg_7_non_zero_addresses.append(avg)


print('')
print('--- INFO ABOUT ADDRESSES ---')
print('')

try:
    print('Total Addresses: {0:12,.3f}'.format(total_addresses_l[-1]))
except:
    print('Total Addresses: ?')
print('')
try:
    print('Active Addresses: {0:12,.3f}'.format(active_addresses_l[-1]))
    print('Active Addresses (avg): {0:12,.3f}'.format(avg_7_active_addresses[-1]))
    print('Max Active Addresses: {0:12,.3f}'.format(max(active_addresses_l)))
except:
    print('Active Addresses: ?')
print('')
try:
    print('New Addresses: {0:12,.3f}'.format(new_addresses_l[-1]))
    print('New Addresses (avg): {0:12,.3f}'.format(avg_7_new_addresses_l[-1]))
    print('Max New Addresses: {0:12,.3f}'.format(max(new_addresses_l)))
except:
    print('New Addresses: ?')
print('')
try:
    print('Non-Zero Addresses: {0:12,.3f}'.format(non_zero_addresses_l[-1]))
    print('Non-Zero Addresses (avg): {0:12,.3f}'.format(avg_7_non_zero_addresses[-1]))
    print('Max Non-Zero Addresses: {0:12,.3f}'.format(max(non_zero_addresses_l)))
except:
    print('Non-Zero Addresses: ?')
print('')


# CHARTS

b = input('Charts (yes/no): ')
if b == 'yes':

    pyplot.subplot(2,2,1)
    pyplot.plot(date_total_addresses_l, total_addresses_l)
    pyplot.plot(date_total_addresses_l, avg_7_total_addresses_l)
    pyplot.xlabel('Date')
    pyplot.ylabel('Total Addresses')
    pyplot.title(crypto)

    pyplot.subplot(2,2,2)
    pyplot.plot(date_active_addresses_l, active_addresses_l)
    pyplot.plot(date_active_addresses_l, avg_7_active_addresses)
    pyplot.xlabel('Date')
    pyplot.ylabel('Active Addresses')
    pyplot.title(crypto)

    pyplot.subplot(2,2,3)
    pyplot.plot(date_new_addresses_l, new_addresses_l)
    pyplot.plot(date_new_addresses_l, avg_7_new_addresses_l)
    pyplot.xlabel('Date')
    pyplot.ylabel('New Addresses')
    pyplot.title(crypto)

    pyplot.subplot(2,2,4)
    pyplot.plot(date_non_zero_addresses_l, non_zero_addresses_l)
    pyplot.plot(date_non_zero_addresses_l, avg_7_non_zero_addresses)
    pyplot.xlabel('Date')
    pyplot.ylabel('Non-Zero Addresses')
    pyplot.title(crypto)

    pyplot.show()

'''
GOAL IS TO SHOW SOME DATA ABOUT ADDRESSES [GOWTH/EVOLUTION] 
'''

# VALUES

print('')
print('--- GET VALUES ABOUT TOTAL ADDRESSES ---')
print('')

month_numb_l = list()
month_perc_l = list()
count = 0
sum_v = 0
avg_l = list()
sum_v_numb = 0
avg_l_numb = list()
for i in range(len(total_addresses_l)):
    v = float(total_addresses_l[i])
    count += 1

    if count % 30 == 0:
        v1 = float(total_addresses_l[i - 29])
        month_v_perc = (v/v1 - 1) * 100
        month_v_numb = v - v1
        sum_v += month_v_perc
        avg_v = round(sum_v / (len(month_perc_l) + 1), 3)
        sum_v_numb += month_v_numb
        avg_v_numb = round(sum_v_numb / (len(month_numb_l) + 1), 3)

        month_perc_l.append(month_v_perc)
        month_numb_l.append(month_v_numb)
        avg_l.append(avg_v)
        avg_l_numb.append(avg_v_numb)

sum_6_months_numb = 0
sum_6_months_perc = 0
for i in range(5):
    v_numb = month_numb_l[-(i+1)]
    v_perc = month_perc_l[-(i+1)]

    sum_6_months_numb += v_numb
    sum_6_months_perc += v_perc

    avg_6_numb = round(sum_6_months_numb / (i+1), 3)
    avg_6_perc = round(sum_6_months_perc / (i+1), 3)

print('Last 6 months Evolutions')
print('')
print('Last month - Number evolution: {0:12,.3f}'.format(month_numb_l[-1]), ' | Monthly perc: ', round(month_perc_l[-1], 3), '%')
print('Month before - Number evolution: {0:12,.3f}'.format(month_numb_l[-2]), ' | Monthly perc: ', round(month_perc_l[-2], 3), '%')
print('Month before - Number evolution: {0:12,.3f}'.format(month_numb_l[-3]), ' | Monthly perc: ', round(month_perc_l[-3], 3), '%')
print('Month before - Number evolution: {0:12,.3f}'.format(month_numb_l[-4]), ' | Monthly perc: ', round(month_perc_l[-4], 3), '%')
print('Month before - Number evolution: {0:12,.3f}'.format(month_numb_l[-5]), ' | Monthly perc: ', round(month_perc_l[-5], 3), '%')
print('Month before - Number evolution: {0:12,.3f}'.format(month_numb_l[-6]), ' | Monthly perc: ', round(month_perc_l[-6], 3), '%')
print('')
print('Monthly growth avg - Number avg: {0:12,.3f}'.format(avg_6_numb), ' | Perc avg: ', avg_6_perc, '%')
print('')
print('All time growth avg per Month - Number avg: {0:12,.3f}'.format(avg_l_numb[-1]), ' | Perc avg : ', avg_l[-1], '%')
print('')



# CHART

a = input('Chart about Total addresses evolution (yes/no): ')
if a == 'yes':

    # CREATE A LIST

    aaaa = list(range(0, len(month_numb_l)))

    pyplot.subplot(1,2,1)
    pyplot.bar(aaaa, month_numb_l)
    pyplot.plot(aaaa, avg_l_numb)
    pyplot.xlabel('Monthly count')
    pyplot.ylabel('Monthly growth by number')
    pyplot.title(crypto)

    pyplot.subplot(1,2,2)
    pyplot.bar(aaaa, month_perc_l)
    pyplot.plot(aaaa, avg_l)
    pyplot.xlabel('Monthly count')
    pyplot.ylabel('% Monthly growth in percentage')
    pyplot.title(crypto)

    pyplot.show()

    print('')
    b = input('Do you wanna see the last months (yes/no): ')
    if b == 'yes':
        b1 = input('Number of months: ')

        for i in range(len(month_numb_l) - int(b1)):
            del month_numb_l[0]
            del month_perc_l[0]

        sum_new_numb = 0
        sum_new_perc = 0
        avg_new_numb_l = list()
        avg_new_perc_l = list()
        for a in range(len(month_numb_l)):
            v_numb = month_numb_l[-(a+1)]
            v_perc = month_perc_l[-(a+1)]

            sum_new_numb += float(v_numb)
            sum_new_perc += float(v_perc)

            avg_new_numb = round(sum_new_numb / (a + 1), 3)
            avg_new_perc = round(sum_new_perc / (a + 1), 3)

            # INSERT LIST

            avg_new_numb_l.append(avg_new_numb)
            avg_new_perc_l.append(avg_new_perc)

        aaaa = list(range(0, len(month_numb_l)))

        pyplot.subplot(1, 2, 1)
        pyplot.bar(aaaa, month_numb_l)
        pyplot.plot(aaaa, avg_new_numb_l)
        pyplot.xlabel('Monthly count')
        pyplot.ylabel('Monthly growth by number')
        pyplot.title(crypto)

        pyplot.subplot(1, 2, 2)
        pyplot.bar(aaaa, month_perc_l)
        pyplot.plot(aaaa, avg_new_perc_l)
        pyplot.xlabel('Monthly count')
        pyplot.ylabel('% Monthly growth in percentage')
        pyplot.title(crypto)

        pyplot.show()


'''
CREATE SOME INDICATORS WITH THIS DATA
'''

print('')
print('--- INDICATORS VALUE ---')
print('')

perc_new_total_l = list()
date_perc_new_total_l = list()
sum_perc_new_total = 0
avg_perc_new_total_l = list()
for i in range(len(new_addresses_l)):
    d1 = date_new_addresses_l[i]
    v1 = new_addresses_l[i]

    n = 0
    d2 = 0
    try:
        while d1 != d2:
            d2 = date_total_addresses_l[n]
            n += 1

        v2 = total_addresses_l[n]

        # MAKE SOME MATH

        perc_new_total = float(v1) / float(v2) * 100
        sum_perc_new_total += perc_new_total
        avg_v_perc_new_total = round(sum_perc_new_total / (len(perc_new_total_l) + 1), 3)

        # INSERT LIST

        perc_new_total_l.append(perc_new_total)
        date_perc_new_total_l.append(d1)
        avg_perc_new_total_l.append(avg_v_perc_new_total)


    except:
        continue

# CREATE AVG

perc_sum = 0
for i in range(len(perc_new_total_l)):
    v = perc_new_total_l[i]
    perc_sum += float(v)

avg_perc = perc_sum / len(perc_new_total_l)

print('Actual % New / Total: {0:12,.3f}'.format(perc_new_total_l[-1]))
print('Avg New / Total: {0:12,.3f}'.format(avg_perc))

# GRAPH

print('')
b = input('Indicator chart (yes/no): ')
if b == 'yes':
    pyplot.plot(date_perc_new_total_l, perc_new_total_l)
    pyplot.plot(date_perc_new_total_l, avg_perc_new_total_l)
    pyplot.xlabel('Date')
    pyplot.ylabel('% New Addresses / Total Addresses')
    pyplot.title(crypto)
    pyplot.show()


print('')
b = input('Data in period of time (yes/no): ')
if b == 'yes':
    c = input('Number of days: ')
    size = len(perc_new_total_l)
    num = int(size - float(c))
    size2 = len(non_zero_addresses_l)
    num2 = int(size2 - float(c))

    for i in range(num):
        del perc_new_total_l[0]
        del date_perc_new_total_l[0]

        del new_addresses_l[0]
        del total_addresses_l[0]
        del active_addresses_l[0]

        del date_active_addresses_l[0]
        del date_new_addresses_l[0]
        del date_total_addresses_l[0]

        del avg_7_total_addresses_l[0]
        del avg_7_active_addresses[0]
        del avg_7_new_addresses_l[0]

    for i in range(num2):
        del non_zero_addresses_l[0]
        del date_non_zero_addresses_l[0]
        del avg_7_non_zero_addresses[0]

    aa = 0
    avg_aa_l = list()
    for i in range(len(perc_new_total_l)):
        aa += perc_new_total_l[i]

        avg_v_aa = round(aa / (i + 1), 3)
        avg_aa_l.append(avg_v_aa)

    avg_aa = aa / len(perc_new_total_l)

    print('')
    print('INFO FOR THE LAST ', c, ' DAYS -------')

    print('')
    print('--- INFO ABOUT INDICATORS ---')
    print('')

    print('Actual % New / Total: {0:12,.3f}'.format(perc_new_total_l[-1]))
    print('Avg New / Total: {0:12,.3f}'.format(avg_aa))

    print('')
    print('--- INFO ABOUT ADDRESSES ---')
    print('')

    try:
        print('Total Addresses: {0:12,.3f}'.format(total_addresses_l[-1]))
    except:
        print('Total Addresses: ?')
    print('')
    try:
        print('Active Addresses: {0:12,.3f}'.format(active_addresses_l[-1]))
        print('Active Addresses (avg): {0:12,.3f}'.format(avg_7_active_addresses[-1]))
        print('Max Active Addresses: {0:12,.3f}'.format(max(active_addresses_l)))
    except:
        print('Active Addresses: ?')
    print('')
    try:
        print('New Addresses: {0:12,.3f}'.format(new_addresses_l[-1]))
        print('New Addresses (avg): {0:12,.3f}'.format(avg_7_new_addresses_l[-1]))
        print('Max New Addresses: {0:12,.3f}'.format(max(new_addresses_l)))
    except:
        print('New Addresses: ?')
    print('')
    try:
        print('Non-Zero Addresses: {0:12,.3f}'.format(non_zero_addresses_l[-1]))
        print('Non-Zero Addresses (avg): {0:12,.3f}'.format(avg_7_non_zero_addresses[-1]))
        print('Max Non-Zero Addresses: {0:12,.3f}'.format(max(non_zero_addresses_l)))
    except:
        print('Non-Zero Addresses: ?')
    print('')
    print('Total Addresses [Start]: {0:12,.3f}'.format(total_addresses_l[0]))
    print('Total Addresses [Finish]: {0:12,.3f}'.format(total_addresses_l[-1]))
    print('Total growth in all period (%): ', round((float(total_addresses_l[-1]) / float(total_addresses_l[0]) - 1) * 100, 3), '%')
    print('Total growth in all period (number): {0:12,.3f}'.format(float(total_addresses_l[-1]) - float(total_addresses_l[0])))
    print('')

    j = input('Chart (yes/no): ')
    if j == 'yes':

        pyplot.subplot(2, 2, 1)
        pyplot.plot(date_total_addresses_l, total_addresses_l)
        pyplot.plot(date_total_addresses_l, avg_7_total_addresses_l)
        pyplot.xlabel('Date')
        pyplot.ylabel('Total Addresses')
        pyplot.title(crypto)

        pyplot.subplot(2, 2, 2)
        pyplot.plot(date_active_addresses_l, active_addresses_l)
        pyplot.plot(date_active_addresses_l, avg_7_active_addresses)
        pyplot.xlabel('Date')
        pyplot.ylabel('Active Addresses')
        pyplot.title(crypto)

        pyplot.subplot(2, 2, 3)
        pyplot.plot(date_new_addresses_l, new_addresses_l)
        pyplot.plot(date_new_addresses_l, avg_7_new_addresses_l)
        pyplot.xlabel('Date')
        pyplot.ylabel('New Addresses')
        pyplot.title(crypto)

        pyplot.subplot(2, 2, 4)
        pyplot.plot(date_non_zero_addresses_l, non_zero_addresses_l)
        pyplot.plot(date_non_zero_addresses_l, avg_7_non_zero_addresses)
        pyplot.xlabel('Date')
        pyplot.ylabel('Non-Zero Addresses')
        pyplot.title(crypto)

        pyplot.show()

        pyplot.plot(date_perc_new_total_l, perc_new_total_l)
        pyplot.plot(date_perc_new_total_l, avg_aa_l)
        pyplot.xlabel('Date')
        pyplot.ylabel('% New Addresses / Total Addresses')
        pyplot.title(crypto)

        pyplot.show()

print('')
print('-- DONE')
print('')
