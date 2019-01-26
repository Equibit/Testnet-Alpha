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
import os
import logging
from collections import namedtuple

# rpc_user and rpc_password are set in the equibit.conf file
#RPCurl = "http://rpc_user:rpc_password@127.0.0.1:18331"
RPCurl = "http://equibit:equibit@dockerhost:18331"

# Add your own addresses to the list in a PR to join the EQB spam network!
addresses = [
    "eqbtestnet1qrappns9a3rvhz6xtegh9nywcazmq3kt08z0ec6", # @macterra/morningstar-1
    "eqbtestnet1qs9zwqh9qlj0z7ut2elkel2czl7weqvlp5dzjzz", # @macterra/xenomorph-1
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

Config = namedtuple('Config', ['use_logger', 'fake'])

def send_eqb(config, conn, i):
    done = False
    attempt = 1

    while (not done) and (attempt <= MAX_RETRIES):
        addr = random.choice(addresses)
        amount = random.randint(1,10000)/1000000.0
        try:
            res = conn.sendtoaddress(addr, amount) if not config.fake else "FAKE"
            bal = conn.getbalance()
            done = True
        except KeyboardInterrupt:
            sys.exit("\n\nInterrupted, exiting.\n")
        except Exception as ex:

            # The node can temporarily become unresponsive.
            # Let's poke the node and resume sending when, and if it wakes up again.

            if attempt == 1:
                log.warning("There was a problem ({}). Retrying for a few minutes.".format(str(ex)))

            attempt += 1

            time.sleep(5)

            if not config.use_logger:
                sys.stdout.write(".") # Let the user know we're still alive and well.
                sys.stdout.flush()

    if done:
        msg = "Tx #{:02d} sent {:.6f} EQB (bal: {:.2f} EQB) to {} in txid {}"
        if config.use_logger:
            log.info(msg.format(i, amount, bal, addr, res))
        else:
            print(msg.format(i, amount, bal, addr[:20], res[:20], end="\r"))
            sys.stdout.flush()

        return True
    else:
        log.error("Unable to recover. Exiting")
        sys.exit("\nUnable to recover. Exiting.\n")
        
def start(config, url, N, delay=1):
    conn = AuthServiceProxy(url) # Initial authentication.
    log.info("Using {} ...".format(url))
    i = 1
    while i <= N:
        time.sleep(delay)
        if send_eqb(config, conn, i):
            i += 1

def get_config():
    global log

    log = logging.getLogger('spam')
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()

    use_logger = False
    env_log = os.environ.get("SPAM_LOG")
    if env_log and env_log.isdigit() and int(env_log) == 1:
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s'))
        use_logger = True

    log.addHandler(handler)

    env_fake = os.environ.get("SPAM_FAKE")
    fake = (env_fake.isdigit() and int(env_fake) == 1) if env_fake else False

    return Config(use_logger=use_logger, fake=fake)


if __name__ == '__main__':
    try:
        rounds = int(input("\nNumber of transactions to send: "))
        interval = int(input("Interval (seconds) between transactions: "))
        config = get_config()
        start(config, RPCurl, rounds, interval)
    except KeyboardInterrupt:
        sys.exit("\n\nInterrupted, exiting.\n")
