import eqb_spam, time

urls = [
    "http://equibit:equibit@127.0.0.1:18331",
    "http://equibit:equibit@127.0.0.1:18332",
    "http://equibit:equibit@127.0.0.1:18333",
]

while True:
    for url in urls:
        eqb_spam.RPCurl = url
        eqb_spam.start(30)
        
    # wait a minute
    for i in range(6):
        for j in range(10):
            time.sleep(1)
            print('.', end='', flush=True)
        print(' ', (i+1)*10)