# EQB Spam Network

These scripts are designed to spam the EQB testnet with small random transactions in order to stress-test the system.

You will need python installed, and also jgarzik's [bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc) package:

```
pip install python-bitcoinrpc
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

That can be done through the normal software development process (branch, edit, commit, push), but we suggest taking the asy route and editing the file directly in github, just make sure you add a good comment when you commit.

## Sender

### eqb_spam

### multi_spam

# Stress-Tester Achievement

