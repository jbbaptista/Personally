import requests
import matplotlib.pyplot as plt
import datetime
import secret

# Constants
ETHERSCAN_API_KEY = secret.api_key_etherscan
TOKEN_ADDRESS = '0x5f18ea482ad5cc6bc65803817c99f477043dce85'
TOP_HOLDERS_COUNT = 10

# Function to get the top holders from Etherscan API
# Function to get the top holders from Etherscan API
def get_top_holders():
    url = f'https://api.etherscan.io/api?module=account&action=tokenholders&contractaddress={TOKEN_ADDRESS}&offset={TOP_HOLDERS_COUNT}&page=1&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url).json()
    print(response)
    top_holders = []

    for holder in response['result']:
        try:
            address = holder['Holder']
            balance = int(holder['Balance'])
            top_holders.append((address, balance))
        except (KeyError, TypeError, ValueError):
            pass

    return top_holders

# Function to get the balance history for each holder
def get_balance_history(holder_address):
    url = f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_ADDRESS}&address={holder_address}&sort=asc&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url).json()
    transfers = response['result']
    timestamps = [int(tx['timeStamp']) for tx in transfers if tx['to'] == holder_address.lower()]
    balances = []
    for i, timestamp in enumerate(timestamps):
        balance = sum(int(tx['value']) for tx in transfers[:i+1] if tx['to'] == holder_address.lower())
        balances.append((timestamp, balance))
    return balances

# Function to plot the balance chart
def plot_balance_chart(balance_histories):
    plt.figure(figsize=(15, 7))

    for address, history in balance_histories.items():
        timestamps = [datetime.datetime.fromtimestamp(entry[0]) for entry in history]
        balances = [entry[1] / 1e18 for entry in history]
        plt.plot(timestamps, balances, label=address)

    plt.title('Top Token Holders Balance Evolution')
    plt.xlabel('Date')
    plt.ylabel('Token Balance')
    plt.legend(title='Top Holders', loc='upper left')
    plt.grid()
    plt.show()

# Main function
def main():
    top_holders = get_top_holders()
    balance_histories = {holder[0]: get_balance_history(holder[0]) for holder in top_holders}
    plot_balance_chart(balance_histories)

if __name__ == '__main__':
    main()
