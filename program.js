
var Client = require('coinbase').Client;

var fs = require("fs");
var content = fs.readFileSync("coinbaseApiKey.json");
var key = JSON.parse(content);

var client = new Client({
    'apiKey': key.apiKey,
    'apiSecret': key.apiSecret
});

client.getAccounts({}, function (err, accounts) {
    console.log('id, created_at, type, crypto_amount, crypto_currency, fiat_amount, fiat_currency')
    accounts.forEach(function (acct) {
        //console.log(acct.name + ': ' + acct.balance.amount + ' ' + acct.balance.currency);
        acct.getTransactions(null, function (err, txns) {
            txns.forEach(function (txn) {
                //https://developers.coinbase.com/api/v2?javascript#transaction-resource
                console.log(txn.id + ', ' + txn.created_at + ', ' + txn.type + ', ' +
                    txn.amount.amount + ', ' + txn.amount.currency + ', ' + txn.native_amount.amount + ', ' + txn.native_amount.currency);

            });
        });

        //https://developers.coinbase.com/api/v2?javascript#deposit-resource
        // acct.getDeposits(null, function(err, txs) {
        //     console.log(txs);
        // });
    });
});