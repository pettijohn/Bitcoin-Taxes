import json
import csv
import io
from datetime import date, datetime
from coinbase.wallet.client import Client

# https://api.coinbase.com/v2/prices/BTC-USD/historic?period=all

# prices = {}

# with open('BTC-USD.json') as btcusd_json:    
#     btcusd_parsed = json.load(btcusd_json)    

#     for pricepoint in btcusd_parsed['data']['prices']:
#         pricedate = datetime.strptime(pricepoint['time'], '%Y-%m-%dT00:00:00Z')
#         prices[pricedate] = pricepoint['price']

# print(prices[datetime(2017, 5, 25)])
    

keys = None
with open('coinbaseApiKey.json') as keys_file:
    keys  = json.load(keys_file)

client = Client(keys['apiKey'], keys['apiSecret'])
accounts = client.get_accounts()
for account in accounts.data:
    # print(account.id)
    txns = client.get_transactions(account.id)
    for tx in txns.data:
        print(tx.id + ', ' + tx.created_at + ', ' + tx.type + ', ' + 
            tx.amount.amount + ', ' + tx.amount.currency + ', ' + tx.native_amount.amount + ', ' + tx.native_amount.currency)

    



