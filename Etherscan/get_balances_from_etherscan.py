import requests
from matplotlib import pyplot as plt
from datetime import datetime
import secret

# KEY FROM ETHERSCAN

api_key = secret.api_key_etherscan

# Get balances

print('')
base_url = 'https://api.etherscan.io/api'
address = input('Insert ethereum address: ')
# address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
ether_value = 10 ** 18

def make_api_url(module, action, address, **kwargs):
    url = base_url + f"?module={module}&action={action}&address={address}&apikey={api_key}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url

def get_account_balance(address):
    get_balance_url = make_api_url("account", "balance", address, tag='latest')
    r = requests.get(get_balance_url)
    response = r.json()

    value = int(response['result']) / ether_value

    return value

# eth = get_account_balance(address)
# print(eth)

# Get transactions

def get_transactions(address):
    get_transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=9999999999, page=1, offset=10000, sort='asc')
    r = requests.get(get_transactions_url)
    response = r.json()['result']

    get_internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=9999999999, page=1, offset=10000, sort='asc')
    r2 = requests.get(get_internal_tx_url)
    response2 = r2.json()['result']

    response.extend(response2)
    response.sort(key=lambda x: int(x['timeStamp']))


    current_balance = 0
    balances = []
    times = []

    for tx in response:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / ether_value
        if "gasPrice" in tx:
            gas = int(tx['gasUsed']) * int(tx['gasPrice']) / ether_value
        else:
            gas = int(tx['gasUsed']) / ether_value

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

        print('--------------')
        print('To:', to)
        print('From:', from_addr)
        print('Value:', value)
        print('Gas:', gas)
        print('Time:', time)

    print('')
    print('Actual Balance:', current_balance)

    aa1 = input('Graph for address balances (yes/no): ')
    if aa1 == 'yes':
        plt.plot(times, balances)
        plt.show()

get_transactions(address)




