import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import secret
from bs4 import BeautifulSoup

ETHERSCAN_API_KEY = secret.api_key
TOKEN_ADDRESS = '0xa735a3af76cc30791c61c10d585833829d36cbe0'
TOKEN_DECIMALS = 18

def get_token_coingecko_id():
    url = f"https://api.coingecko.com/api/v3/search?query={TOKEN_ADDRESS}"
    response = requests.get(url)
    data = response.json()
    try:
        return data['coins'][0]['item']['id']
    except IndexError:
        print("Token not found on CoinGecko.")
        return None

def get_token_price_usd(token_coingecko_id):
    if token_coingecko_id is None:
        return None

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_coingecko_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[token_coingecko_id]['usd']

TOKEN_COINGECKO_ID = get_token_coingecko_id()
TOKEN_PRICE_USD = get_token_price_usd(TOKEN_COINGECKO_ID)

if TOKEN_PRICE_USD is None:
    print("Cannot fetch token price. Please enter the current token price manually.")
    TOKEN_PRICE_USD = float(input("Enter the current token price in USD: "))
else:
    print(f"Current token price in USD: {TOKEN_PRICE_USD}")

def get_token_transactions():
    txs = []
    page = 1
    while True:
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN_ADDRESS}&page={page}&offset=100&sort=asc&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url)
        data = response.json()
        result = data['result']
        if not result:
            break
        txs.extend(result)
        page += 1
    return txs

def is_smart_contract(address):
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['result'] != '0x'

def get_token_holders(token_address, etherscan_url="https://etherscan.io/token/generic-tokenholders2"):
    holder_data = []
    page = 1
    more_data = True

    while more_data:
        url = f"{etherscan_url}?a={token_address}&p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find("table")
        if not table:
            more_data = False
            break

        rows = table.find_all("tr")
        if len(rows) <= 1:
            more_data = False
            break

        for row in rows[1:]:
            columns = row.find_all("td")
            if len(columns) < 3:
                continue

            address = columns[1].text.strip()
            balance = columns[2].text.strip().split(" ")[0].replace(",", "")
            holder_data.append((address, float(balance)))

        page += 1

    return holder_data


def print_top_holders(holder_data, top=10):
    sorted_data = sorted(holder_data, key=lambda x: x[1], reverse=True)
    print(f"Top {top} holders:")
    for i, (address, balance) in enumerate(sorted_data[:top], start=1):
        print(f"{i}. Address: {'*' * len(address)}, Balance: {'*' * len(str(balance))}")


def analyze_token():
    holders = get_token_holders(TOKEN_ADDRESS)

    print_top_holders(holders)

    whale_activity = []

    for address, balance in holders:
        value_in_usd = balance * TOKEN_PRICE_USD
        if value_in_usd > 100000:
            whale_activity.append((address, balance))
            print(
                f"Whale found: {'*' * len(address)}, Balance: {'*' * len(str(balance))}, Value in USD: {value_in_usd}")

    if whale_activity:
        print(f"Number of whales: {len(whale_activity)}")
    else:
        print("No whale activity found.")


if __name__ == "__main__":
    analyze_token()

