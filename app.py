from binance.cm_futures import CMFutures
import logging
import os
KEY_FILE = 'credentials.txt'

# Загрузить данные токена
if os.path.exists(KEY_FILE):
    f = open(KEY_FILE, "r")
    contents = []
    if f.mode == 'r':
        contents = f.read().split('\n')
    BINANCE_KEYS = dict(KEY=contents[0], SECRET=contents[1])
else:
    logging.error("Did not find token file")
    exit(1)


cm_futures_client = CMFutures()

# get server time
print(cm_futures_client.time())

cm_futures_client = CMFutures(key=BINANCE_KEYS['KEY'], secret=BINANCE_KEYS['SECRET'])

# Get account information
print(cm_futures_client.account())

# Post a new order
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.002,
    'price': 59808
}

response = cm_futures_client.new_order(**params)
print(response)