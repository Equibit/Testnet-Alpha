# Sends small random transactions to random addresses
#
# Depends on https://github.com/jgarzik/python-bitcoinrpc
# pip install python-bitcoinrpc

from __future__ import print_function
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import random
import datetime
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
    ]

auth = AuthServiceProxy(RPCurl) # Initial authentication.

def send_eqb():
    addr = random.choice(addresses)
    amount = random.randint(1,10000)/1000000.0
    try:
        res = auth.sendtoaddress(addr, amount)
        bal = auth.getbalance()
        return " sent {:.6f} EQB (remaining balance: {:.2f} EQB) to {}... in txid {}...".format(amount, bal, addr[:20], res[:20])
    except KeyboardInterrupt:
        sys.exit("\n\nInterrupted, exiting.\n")
    except Exception:
        print("\n\nThere was a problem. Retrying for a few minutes.\n")

        # The node can temporarily become unresponsive.
        # Let's poke the node and resume sending when, and if it wakes up again.
        x = 0
        while x < 180:
            time.sleep(5)
            sys.stdout.write(".") # Let the user know we're still alive and well.
            sys.stdout.flush()
            try:
                res = auth.sendtoaddress(addr, amount)
                bal = auth.getbalance()
                print("\n\nRecovered, resuming ...\n")
                break
            except:
                x += 5
        if x != 180:
            return " sent {:.6f} EQB (remaining balance: {:.2f} EQB) to {}... in txid {}...".format(amount, bal, addr[:$
        else:
            sys.exit("\nUnable to recover. Exiting.\n")
        
def start(N, t):
    i = 0
    print("\nUsing {} ...\n".format(RPCurl))
    while i <= N-1:
        time.sleep(t)
        log = send_eqb()
        if log:
            i += 1
            print("Tx #" + str(i) + log, end="\r")
            sys.stdout.flush()
    print("")

if __name__ == '__main__':
    try:
        rounds = input("\nNumber of transactions to send: ")
        interval = input("Interval (seconds) between transactions: ")
        start(rounds, interval)
    except KeyboardInterrupt:
        sys.exit("\n\nInterrupted, exiting.\n")
