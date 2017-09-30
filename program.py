import json
import csv
import io
import re
from pathlib import Path
from datetime import date, datetime
from coinbase.wallet.client import Client
from decimal import *
import rules

class RunningTotal:

    # Define the crypto currency, e.g. BTC or ETH
    def __init__(self, cryptoCurrency):
        self.cryptoCurrency = cryptoCurrency

    cryptoCurrency = ""
    cryptoBalance = 0
    fiatTotalExpense = 0
    fiatCurrency = "USD"

    def getCostBasis(self):
        return self.fiatTotalExpense / self.cryptoBalance 

class CryptoCurrency:
    BTC = "BTC"
    ETH = "ETH"

class TxType:
    BUY = "buy"
    SEND = "send"
    SELL = "sell"
    TRANSFER = "transfer"
    EXCHANGE_DEPOSIT = "exchange_deposit"
    EXCHANGE_WITHDRAWAL = "exchange_withdrawal"
    VAULT_WITHDRAWAL = "vault_withdrawal"
    fiat_withdrawal = "fiat_withdrawal"

class TxField:
    TYPE = "type"
    CRYPTOCURRENCY = "amount.currency"
    CRYPTOAMOUNT = "amount.amount"
    FIATCURRENCY = "native_amount.currency"
    FIATAMOUNT = "native_amount.amount"
    

# A column name uses dot syntax to step into nested dictionaries. 
# Recursively walk the dots and return the value.
def getSubcolumn(valsDics, id):
    if re.search("\.", id):
        matches = re.search("^([^\.]+)\.(.*)$", id)
        start = matches[1]
        remainder = matches[2]
        return getSubcolumn(valsDics[start], remainder)
    else:
        return valsDics[id]

p = Path('./data/')
if not p.exists():
    p.mkdir()

p = Path('./data/coinbaseCache.json')
if not p.exists():
    #Fetch all transaction data from Coinbase if we don't have a local cache
    keys = None
    with open('coinbaseApiKey.json') as keys_file:
        keys  = json.load(keys_file)

    client = Client(keys['apiKey'], keys['apiSecret'])
    accounts = client.get_accounts()

    alltxns = []

    for account in accounts.data:
        txns = client.get_transactions(account.id, limit=25)
        alltxns += txns.data
        while True: 
            if txns.pagination.next_uri != None:
                # next_uri='/v2/accounts/7e421ebf-9b0f-5b40-b0ef-c4d82c9d943e/transactions?starting_after=3a42e194-ef17-50a6-bafe-c946c0b7dfd5'
                starting_after_guid = re.search('starting_after=([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})', txns.pagination.next_uri, re.I)[1]
                txns = client.get_transactions(account.id, limit=25, starting_after=starting_after_guid)
                alltxns += txns.data
            else:
                break

    # Save all of the transactions to a cache 
    print(json.dumps(alltxns))
    with open('./data/coinbaseCache.json', 'w') as cache:
        cache.write(json.dumps(alltxns))


#Now we have all transactions locally
with open('./data/coinbaseCache.json', 'r') as cache:
    rawData = json.loads(cache.read())

    data = sorted(rawData, key=lambda tx: tx['created_at'])

    runningTotalBTC = RunningTotal(CryptoCurrency.BTC)
    runningTotalETH = RunningTotal(CryptoCurrency.ETH)

    for tx in data:

        if getSubcolumn(tx, TxField.TYPE) == TxType.BUY:
            rt = runningTotalBTC if getSubcolumn(tx, TxField.CRYPTOCURRENCY) == CryptoCurrency.BTC else runningTotalETH
            rt.cryptoBalance += Decimal(getSubcolumn(tx, TxField.CRYPTOAMOUNT))
            rt.fiatTotalExpense += Decimal(getSubcolumn(tx, TxField.FIATAMOUNT))

    pass
    foo = runningTotalBTC.getCostBasis()



    # rules = [rules.MiningIncome()]
    
    # for tx in data:
    #     for rule in rules:
    #         rule.matches(tx)

    # balancesCrypto = {}
    # balancesFiat = {}

    # # Use a simple JSON file to transform the inputs to an output CSV
    # # This makes adding separate outputs easily config-driven
    # transforms = None
    # with open('transforms.json') as keys_file:
    #     transforms = json.load(keys_file)
    # transform = transforms[0]
    # transColumns = transform['columns']

    # with open('./output.csv', 'w', newline='', encoding='utf-8') as outputfile:
    #     # The automatic tranform columns are separate from the manually-added columns
    #     csvColumns = transColumns.copy()
    #     csvColumns.append("runningTotalNativeCurrency")
    #     csvColumns.append("runningTotalCrypto")
    #     outputcsv = csv.DictWriter(outputfile, csvColumns)
    #     outputcsv.writeheader()

    #     for tx in data:
    #         cryptoCurrency = tx['amount']['currency']
    #         amount = Decimal(tx['amount']['amount'])

    #         fiatCurrency = tx['native_amount']['currency']
    #         fiatAmount = Decimal(tx['native_amount']['amount'])
            
    #         if balancesCrypto.get(cryptoCurrency) == None:
    #             balancesCrypto[cryptoCurrency] = Decimal(0)
    #         balancesCrypto[cryptoCurrency] += amount

    #         if balancesFiat.get(fiatCurrency) == None:
    #             balancesFiat[fiatCurrency] = Decimal(0)
    #         balancesFiat[fiatCurrency] += fiatAmount
            
    #         # buy, send, sell, transfer, 
    #         # exchange_deposit, exchange_withdrawal, 
    #         # vault_withdrawal, fiat_withdrawal
    #         lineDict = {}
    #         for column in transColumns:
    #             lineDict[column] = getSubcolumn(column, tx)

    #         lineDict["runningTotalNativeCurrency"] = balancesFiat["USD"]
    #         lineDict["runningTotalCrypto"] = balancesCrypto[cryptoCurrency]
    #         outputcsv.writerow(lineDict)

    #     pass

    