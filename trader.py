key = ''
secret = ''

import urllib.parse
import hashlib
import hmac
import base64
import time
import json
import requests

nonce = lambda: int(time.time()*1000000)

def signature(urlpath, data):

    if isinstance(data, str):
        encoded = (str(json.loads(data)["nonce"]) + data).encode()
    else:
        encoded = (str(data["nonce"]) + urllib.parse.urlencode(data)).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def limit_buy(pair, price, volume, cl_ord_id='ClassOf2013'):
    payload = json.dumps({
      "nonce": nonce(),
      "ordertype": "limit",
      "type": "buy",
      "volume": volume,
      "pair": pair,
      "price": price,
      "cl_ord_id": cl_ord_id
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'API-Key': key,
      'API-Sign': signature("/0/private/AddOrder", payload)
    }

    resp = requests.post("https://api.kraken.com/0/private/AddOrder", headers=headers, data=payload).json()
    print(resp)

def market_buy(pair, volume, cl_ord_id='ClassOf2013'):
    payload = json.dumps({
      "nonce": nonce(),
      "ordertype": "market",
      "type": "buy",
      "volume": volume,
      "pair": pair
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'API-Key': key,
      'API-Sign': signature("/0/private/AddOrder", payload)
    }

    resp = requests.post("https://api.kraken.com/0/private/AddOrder", headers=headers, data=payload).json()
    print(resp)


market_buy("XBTUSD", 0.00005)
    
