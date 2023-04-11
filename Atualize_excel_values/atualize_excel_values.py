import openpyxl
import requests
import time
import pprint
import datetime

'''
GET INFO FROM EXCEL, 
ATUALIZE THE VALUES OF TOKENS OPPORTUNITIES EXCEL
'''

print('')
print('Starting Algorithm ')
print('')

# Open excel sheet

workbook = openpyxl.load_workbook('/Users/jbbaptista/Documents/Secret/Finance/ATIS Capital/Trading/Analysis/Tokens opportunities.xlsx')
worksheet = workbook['Sheet1']

# Read the excel document and get important info

a = True
i = 5
days_ago = 30
current_time = datetime.datetime.now()
start_date = current_time - datetime.timedelta(days=days_ago)
while a == True:
    i += 1

    # Get crypto name

    Location = 'B' + str(i)
    crypto_name = worksheet[Location].value
    l1 = 'B' + str(i + 1)
    next_name = worksheet[l1].value



    # Stop the algo

    if next_name == None:
        a = False

    # Get API name

    Location1 = 'D' + str(i)
    coingecko_api = str(worksheet[Location1].value)

    # GET important values to insert

    url = 'https://api.coingecko.com/api/v3/coins/' + coingecko_api + '?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'
    url2 = f'https://api.coingecko.com/api/v3/coins/{coingecko_api}/market_chart/range?vs_currency=usd&from={start_date.timestamp()}&to={current_time.timestamp()}'
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 429:
            print('')
            print('Exceeded rate limit - Waiting 120sec to continue')
            time.sleep(120)
            print('-- Continue')
            print('')
            r = requests.get(url)

    try:
        r2 = requests.get(url2)
        r2.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 429:
            print('')
            print('Exceeded rate limit - Waiting 120sec to continue')
            time.sleep(120)
            print('-- Continue')
            print('')
            r2 = requests.get(url2)

    response = r.json()
    response2 = r2.json()

    market_cap = round(float(response['market_data']['market_cap']['usd']) / 1000000, 3)
    fdv = round(float(response['market_data']['total_supply']) * float(response['market_data']['current_price']['usd']) / 1000000, 3)
    try:
        tvl = round(float(response['market_data']['total_value_locked']['usd']) / 1000000, 3)
    except:
        tvl = None

    market_cap_30days = round(float(response2['market_caps'][0][1]) / 1000000, 3)

    print(crypto_name, '//', 'MCap:', market_cap, 'M //', 'MCap 30D:', market_cap_30days, 'M //', 'FDV:', fdv, 'M //', 'TVL:', tvl, 'M')

    # Update MarketCap value in excel

    cell_market_cap = 'G' + str(i)

    cell = worksheet[cell_market_cap]
    original_format = cell.number_format

    cell.value = market_cap
    cell.number_format = original_format

    # Update the MarketCap 30days value in excel

    cell_market_cap_30days = 'H' + str(i)

    cell = worksheet[cell_market_cap_30days]
    original_format = cell.number_format

    cell.value = market_cap_30days
    cell.number_format = original_format

    # Update FDV value in excel

    cell_fdv = 'M' + str(i)

    cell = worksheet[cell_fdv]
    original_format = cell.number_format

    cell.value = fdv
    cell.number_format = original_format

    # Update TVL

    if tvl != None:
        cell_tvl = 'V' + str(i)

        cell = worksheet[cell_tvl]
        original_format = cell.number_format

        cell.value = tvl
        cell.number_format = original_format


    workbook.save('/Users/jbbaptista/Documents/Secret/Finance/ATIS Capital/Trading/Analysis/Tokens opportunities.xlsx')

print('')
print('-- Values updated ')
print('')





