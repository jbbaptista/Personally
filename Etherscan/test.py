import requests
import secret

token_address = '0x5f18ea482ad5cc6bc65803817c99f477043dce85'
etherscan_api = secret.api_key_etherscan
contract_address = '0x4255eBE7ddbE1097a3692a48249C7d344A0Af618'

url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={token_address}&tag=latest&apikey={etherscan_api}'

r = requests.get(url)
response = r.json()

print(response)

