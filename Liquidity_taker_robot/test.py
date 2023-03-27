import json
import hmac
import time
from urllib.parse import quote_plus
import bybit
import websocket
import secret

'''

The goal é tentar comunicar com a API da bybit e com a WS da bybit

Receber:
    Asks e Bids colocadas no mercado da Api da Bybit
    Capital em ETH

    Asks e Bids do mercado websocket

'''

# Make a connection with websocket bybit

ws_url = 'wss://stream.bybit.com/realtime'

api_key = secret.bybit()['api_key']
secret_key = secret.bybit()['secret_key']

# Generate expires

expires = int((time.time() + 1) * 1000)

#Generate signature

signature = str(
    hmac.new(
        bytes(secret_key, 'utf-8'),
        bytes(f'GET/realtime{expires}', 'utf-8'),
        digestmod='sha256'
    ).hexdigest()
)

param = f'api_key={api_key}&expires={expires}&signature={signature}'.format(
    api_key = api_key,
    expires = expires,
    signature = signature
)

url = ws_url + '?' + param

ws = websocket.WebSocketApp(
    url = url
)


'''
VER DAQUI PARA A FRENTE
'''

ws.send(
    json.dumps({
        "op": "auth",
        "args": [api_key, expires, signature]
    })
)

