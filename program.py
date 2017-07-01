import json
import csv
import io
import re
from pathlib import Path
from datetime import date, datetime
from coinbase.wallet.client import Client


p = Path('./data/')
if not p.exists():
    p.mkdir()

p = Path('./data/coinbaseCache.json')
if not p.exists():

    keys = None
    with open('coinbaseApiKey.json') as keys_file:
        keys  = json.load(keys_file)

    client = Client(keys['apiKey'], keys['apiSecret'])
    accounts = client.get_accounts()

    alltxns = []

    print('account, txid, created_at, type, crypto_amount, crypto_currency, fiat_amount, fiat_currency')

    for account in accounts.data:
        # print(account.id)
        txns = client.get_transactions(account.id, limit=25)
        for tx in txns.data:
            alltxns.append(tx)
        while True: 
            
            for tx in txns.data:
                print(account.id + ', ' + tx.id + ', ' + tx.created_at + ', ' + tx.type + ', ' + 
                    tx.amount.amount + ', ' + tx.amount.currency + ', ' + tx.native_amount.amount + ', ' + tx.native_amount.currency)

            if txns.pagination.next_uri != None:
                # next_uri='/v2/accounts/7e421ebf-9b0f-5b40-b0ef-c4d82c9d943e/transactions?starting_after=3a42e194-ef17-50a6-bafe-c946c0b7dfd5'
                starting_after_guid = re.search('starting_after=([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})', txns.pagination.next_uri, re.I)[1]
                txns = client.get_transactions(account.id, limit=25, starting_after=starting_after_guid)
                for tx in txns.data:
                    alltxns.append(tx)
            else:
                break

    # Save all of the transactions to a cache 
    print(json.dumps(alltxns))
    with open('./data/coinbaseCache.json', 'w') as cache:
        cache.write(json.dumps(alltxns))

with open('./data/coinbaseCache.json', 'r') as cache:
    data = json.loads(cache.read())
    pass
