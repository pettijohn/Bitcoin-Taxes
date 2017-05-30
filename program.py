import json
import csv
import io
from datetime import date, datetime

# https://api.coinbase.com/v2/prices/BTC-USD/historic?period=all

with open('BTC-USD.json') as btcusd_json:    
    btcusd_parsed = json.load(btcusd_json)

    prices = {}

    for pricepoint in btcusd_parsed['data']['prices']:
        pricedate = datetime.strptime(pricepoint['time'], '%Y-%m-%dT00:00:00Z')
        prices[pricedate] = pricepoint['price']

    print(prices[datetime(2017, 5, 25)])
