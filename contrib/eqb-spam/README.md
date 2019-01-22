# EQB Spam Network

These scripts are designed to spam the EQB testnet with small random transactions in order to stress-test the system.

You will need python3 installed, and also jgarzik's [bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc) package:

```
pip3 install python-bitcoinrpc
```

There are two ways to join the Spam Network, as a sender and as a receiver (ideally both). You will need some EQB in your wallet to participate as a sender, either through mining or accumulated as a receiver before becoming a sender.

## Receiver

To become a receiver first generate one or more eqbtestnet addresses:

```
david@Deadpool:~/Equibit$ equibit-cli -datadir=[folder] getnewaddress spam bech32
tq1qpn5ptsek6la658g5640qckghe4n3znz7aqz0dj
```

Then add your address(es) to [eqb_spam.py](eqb_spam.py) to the list directly in the python code:

```
# Add your own addresses to the list in a PR to join the EQB spam network!
addresses = [
    "eqbtestnet1qx7m4ja35j5vsflvrywhrd3wznezfnj86khfqw4", # @macterra/star-lord-1
    "eqbtestnet1qettj7geg32mepyd44qxdnsmudtnvau66qgpse3", # @macterra/star-lord-2
    "eqbtestnet1q5xjschuuhhvnuwe0zp54xd5gtma3ygrtvhydfd", # @macterra/star-lord-3
]
```

That can be done through the normal software development process (branch, edit, commit, push), but we suggest taking the easy route and editing the file directly in github, just make sure you add a good comment when you commit.

## Sender

There are two scripts for sending transactions. Use eqb_spam if you have a single node, use multi_spam if you have two or more spam nodes. The multi_spam script uses eqb_spam so you'll have to download both.

Either clone this repo to get the scripts or download them directly to a new folder.

### eqb_spam

Edit the script and check the defaults (if you changed the node's default user, password or port in the configuration file you'll have to update the script).

Using the default values hard-coded in the script it will send between 0.000001 and 0.0099999 EQB to an address chosen randomly from the list. The script will ask how many transactions to send before exiting. You should also specify the interval at which the transactions will be sent.

Then run it with python:
```
python3 eqb_spam.py
Using http://equibit:equibit@127.0.0.1:18331 ...
0 sent 0.007138 to eqbtestnet1q5xjschuuhhvnuwe0zp54xd5gtma3ygrtvhydfd in txid d667f3c431f682fc6be23bfea6bd09d08275fc4ec0aaad5d3b12e65201f79a85
1 sent 0.005273 to eqbtestnet1qx7m4ja35j5vsflvrywhrd3wznezfnj86khfqw4 in txid 0dc0fc80b0378cbf72ddf2cd54ae70cba96b08d3364d17e0e297bcf3ec458c9d
2 sent 0.007801 to eqbtestnet1qx7m4ja35j5vsflvrywhrd3wznezfnj86khfqw4 in txid efa19ef1bf05a01b3469b09da56a24f9908c3a3fb3d43e92a802e2ab21d26674
3 sent 0.007832 to eqbtestnet1q5xjschuuhhvnuwe0zp54xd5gtma3ygrtvhydfd in txid 846a074ca9237c27db6e9a7d34995268f581094e59ff7acd4c85549fe947f17d
4 sent 0.007313 to eqbtestnet1qx7m4ja35j5vsflvrywhrd3wznezfnj86khfqw4 in txid 77b3859534e5fc75bde8bc51578d233a95aee0b2233ec32b713532d3645e3c43
5 sent 0.008725 to eqbtestnet1qettj7geg32mepyd44qxdnsmudtnvau66qgpse3 in txid 2871ca081fee676e50cc54ccb112699672385a73863d5482f6c1d891875fcbad
6 sent 0.007799 to eqbtestnet1q5xjschuuhhvnuwe0zp54xd5gtma3ygrtvhydfd in txid 93ec1a6567be253c4456b3a22592e60534d537b721867517ea363645c37c327e
7 sent 0.001681 to eqbtestnet1qx7m4ja35j5vsflvrywhrd3wznezfnj86khfqw4 in txid 4050887306e3e01127f4d89cb55d0feb5e26573a55096cd92e7dfb472bf3a250
8 sent 0.003091 to eqbtestnet1q5xjschuuhhvnuwe0zp54xd5gtma3ygrtvhydfd in txid 5d28990e23652e67aad5b438374cf3e5bf6500d48e26764b1680edeb0129a334
9 sent 0.003438 to eqbtestnet1qettj7geg32mepyd44qxdnsmudtnvau66qgpse3 in txid 9bfd4a3e6992b58cd1b60830bf5684779699e5fec5354e475bd7a1e775903a55
```

If the wallet runs out of funds to send it will simply exit before reaching the specified number of iterations. THIS OFTEN HAPPENS WAY SOONER THAN EXPECTED. The issue is that when you send funds you always send more in terms of UTXOs, some goes to miner fees and the rest comes back in change in a single UTXO. You can spend the change before it is confirmed in a block, but only up to a chain of 25 in the mempool (this is a limit inherited from bitcoin core). 

If you hit that limit your wallet will appear to have a zero balance. DON'T PANIC. Even if `getwalletinfo` shows zero balance you can use the `listaccounts` CLI command to show the true balance. You just have to wait until some of those change UTXOs get confirmed in the next block to free up some UTXOs to spend again.

### multi_spam

This script simply cycles through two or more nodes, calling eqb_spam for each one in turn. At the end of a cycle it waits a minute before starting the next cycle. This script was developed to address the problem describe above where a node runs out of funds to send due to the limit of the number of change transactions that can exist in the mempool at a given time. It seems to take a fair abount of time before a node's wallet builds up enough small UTXOs to run eqb_spam continuously.

Edit the script to configure it for your nodes then run it with python:

```
python3 multi_spam.py
```



