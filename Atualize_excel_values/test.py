import requests
import datetime

# Set the parameters for the API request
coin_id = 'matic-network'
days_ago = 30
current_time = datetime.datetime.now()
start_date = current_time - datetime.timedelta(days=days_ago)

# Format the start and end dates for the API request
start_date_str = start_date.strftime("%d-%m-%Y")
end_date_str = current_time.strftime("%d-%m-%Y")

# Send the API request to get the historical market data
url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from={start_date.timestamp()}&to={current_time.timestamp()}'
response = requests.get(url)

# Parse the API response to get the market cap data
market_cap_data = response.json()['market_caps']

# Get the market cap value 30 days ago
market_cap_30_days_ago = market_cap_data[0][1]

print(f"The market cap of {coin_id} 30 days ago ({start_date_str}) was ${market_cap_30_days_ago:,.2f}")

