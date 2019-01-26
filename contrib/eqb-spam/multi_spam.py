#!/usr/bin/env python3
import eqb_spam, time

urls = [
    "http://rpc_user:rpc_password@127.0.0.1:18331"
#,
#    "http://equibit:equibit@127.0.0.1:18332",
#    "http://equibit:equibit@127.0.0.1:18333",
]

while True:
    for url in urls:
        eqb_spam.start(url, 30, 1)
        
    # wait a minute
    for i in range(6):
        for j in range(10):
            time.sleep(1)
            print('.', end='', flush=True)
        print(' ', (i+1)*10)
