# Sends a small random transaction to a random address
#
# Depends on https://github.com/jgarzik/python-bitcoinrpc
# pip install python-bitcoinrpc

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import random

# rpc_user and rpc_password are set in the bitcoin.conf file
RPCurl = "http://equibit:equibit@127.0.0.1:18331"

# Add your own addresses to the list in a PR to join the EQB spam network!
addresses = [
    "eqbtestnet1qx7m4ja35j5vsflvrywhrd3wznezfnj86khfqw4", # @macterra/star-lord-1
    "eqbtestnet1qettj7geg32mepyd44qxdnsmudtnvau66qgpse3", # @macterra/star-lord-2
    "eqbtestnet1q5xjschuuhhvnuwe0zp54xd5gtma3ygrtvhydfd", # @macterra/star-lord-3
    "eqbtestnet1q7z83eksyceecdyfsz43z7pqw9c475mmlan6kh4", # @Jorgeminator/Statsy
    ]

rpc_connection = AuthServiceProxy(RPCurl)

def send_eqb():
    addr = random.choice(addresses)
    amount = random.randint(1,10000)/1000000.0
    try:
        res = rpc_connection.sendtoaddress(addr, amount)    
        return "sent {:.6f} to {} in txid {}".format(amount, addr, res)
    except:
        return None

def start(N):
    print("Using {} ...".format(RPCurl))
    for i in range(N):
        log = send_eqb()
        if log:
            print(i, log)
        else:
            break
    
if __name__ == '__main__':
    start(10)
