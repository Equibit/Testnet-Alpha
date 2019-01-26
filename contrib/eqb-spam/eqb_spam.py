#!/usr/bin/env python3
# Sends small random transactions to random addresses
#
# Depends on https://github.com/jgarzik/python-bitcoinrpc
# pip install python-bitcoinrpc

from __future__ import print_function
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import random
import time
import sys

# rpc_user and rpc_password are set in the equibit.conf file
RPCurl = "http://rpc_user:rpc_password@127.0.0.1:18331"

# Add your own addresses to the list in a PR to join the EQB spam network!
addresses = [
    "eqbtestnet1qx7m4ja35j5vsflvrywhrd3wznezfnj86khfqw4", # @macterra/star-lord-1
    "eqbtestnet1qettj7geg32mepyd44qxdnsmudtnvau66qgpse3", # @macterra/star-lord-2
    "eqbtestnet1q5xjschuuhhvnuwe0zp54xd5gtma3ygrtvhydfd", # @macterra/star-lord-3
    "eqbtestnet1q4n3my2cnh92rhmtauu5lfufj2qat32wxn4ja7e", # @macterra/deadpool-1
    "eqbtestnet1q2zl38kysmudqkzhc9x2asj9q80wwylrw9ptsnp", # @macterra/deadpool-2
    "eqbtestnet1qmsahc26h2a0azk9z43m5w5htqklr2e5t5svynl", # @macterra/deadpool-3
    "eqbtestnet1q7z83eksyceecdyfsz43z7pqw9c475mmlan6kh4", # @Jorgeminator/Statsy
    "eqbtestnet1q5rvfa3rnx9dykk3cg35fzq86aczh3ed4y0l8vu", # @pete/peteminer-1
    "eqbtestnet1qrucy65lehr67pjeg88gmse7k055la77j8dysmv", # @pete/peteminer-2
    "eqbtestnet1q7qsm0hn5sw456kf34mu3hhcy5lzcy5jfm29rda", # @pete/peteminer-3
    "eqbtestnet1qzmje7kkk6d2hdmxwhfz0ypqxt69jcfl3w5wxrp", # @darvs/jupiter-mining-1
    ]

MAX_RETRIES = 36

conn = None # Connection

def send_eqb():

    done = False
    attempt = 1

    while (not done) and (attempt <= MAX_RETRIES):
        addr = random.choice(addresses)
        amount = random.randint(1,10000)/1000000.0
        try:
            res = conn.sendtoaddress(addr, amount)
            bal = conn.getbalance()
            done = True
        except KeyboardInterrupt:
            sys.exit("\n\nInterrupted, exiting.\n")
        except Exception as ex:

            # The node can temporarily become unresponsive.
            # Let's poke the node and resume sending when, and if it wakes up again.

            if attempt == 1:
                print("\n\nThere was a problem (%s). Retrying for a few minutes.\n" % str(ex))

            time.sleep(5)
            attempt += 1

            sys.stdout.write(".") # Let the user know we're still alive and well.
            sys.stdout.flush()

    if done:
        return " sent {:.6f} EQB (remaining balance: {:.2f} EQB) to {}... in txid {}...".format(amount, bal, addr[:20], res[:20])
    else:
        sys.exit("\nUnable to recover. Exiting.\n")
        
def start(url, N, delay=1):
    global conn
    conn = AuthServiceProxy(url) # Initial authentication.
    print("\nUsing {} ...\n".format(url))
    i = 0
    while i < N:
        time.sleep(delay)
        log = send_eqb()
        if log:
            i += 1
            print("Tx #" + str(i) + log, end="\r")
            sys.stdout.flush()
    print("")

if __name__ == '__main__':
    try:
        rounds = int(input("\nNumber of transactions to send: "))
        interval = int(input("Interval (seconds) between transactions: "))
        start(RPCurl, rounds, interval)
    except KeyboardInterrupt:
        sys.exit("\n\nInterrupted, exiting.\n")
