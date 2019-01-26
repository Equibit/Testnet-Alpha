#!/usr/bin/env python3
import eqb_spam, time, os

default_urls = [
    "http://equibit:equibit@127.0.0.1:18331",
    "http://equibit:equibit@127.0.0.1:18332",
    "http://equibit:equibit@127.0.0.1:18333",
]

config = eqb_spam.get_config()

while True:
    env_urls = os.environ.get("SPAM_URLS")
    urls = env_urls.replace(" ", "").split(";") if env_urls else default_urls

    for url in urls:
        eqb_spam.start(config, url, 30, 1)
    
    # wait a minute
    if config.use_logger:
        time.sleep(60)
    else:
        for i in range(6):
            for j in range(10):
                time.sleep(1)
                print('.', end='', flush=True)
            print(' ', (i+1)*10)


