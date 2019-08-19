from . import app
import requests
from . import redis_store
import json


HOST = 'http://www.pse.com.ph/stockMarket/home.html'
HEADERS = {'Referer': HOST}

def retrieve_stocks():
    print("Getting new stocks")
    try:
        r = requests.get(HOST + '?method=getSecuritiesAndIndicesForPublic&ajax=true', headers=HEADERS, timeout=5)
        stocks = r.json()
        stocks = json.dumps(stocks[1:])
        redis_store.set('stocks:all', stocks)
    except requests.exceptions.Timeout as err:
         print(err)    
