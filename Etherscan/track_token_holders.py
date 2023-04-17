from web3 import Web3, HTTPProvider
import secret

API_KEY = secret.api_key_infura
INFURA_URL = f'https://mainnet.infura.io/v3/{API_KEY}'

w3 = Web3(HTTPProvider(INFURA_URL))

TOKEN_CONTRACT = "0x6b175474e89094c44da98b954eedeac495271d0f"
TOKEN_HOLDER = "0xf326e4de8f66a0bdc0970b79e0924e33c79f1915"

balanceOfABI = [
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
]

def get_token_balance(token_contract, token_holder):
    contract = w3.eth.contract(address=Web3.toChecksumAddress(token_contract), abi=balanceOfABI)
    balance = contract.functions.balanceOf(Web3.toChecksumAddress(token_holder)).call()
    formatted_balance = w3.fromWei(balance, "ether")
    return formatted_balance

if __name__ == "__main__":
    balance = get_token_balance(TOKEN_CONTRACT, TOKEN_HOLDER)
    print(balance)
