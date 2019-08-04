from . import app
import requests
import json


HOST = 'http://www.pse.com.ph/stockMarket/home.html'
HEADERS = {'Referer': HOST}

def retrieve_stocks():
    print("Getting new stocks")
    try:
        r = requests.get(HOST + '?method=getSecuritiesAndIndicesForPublic&ajax=true', headers=HEADERS, timeout=5)
        stocks = r.json()
        return json.dumps(stocks)
    except requests.exceptions.Timeout as err:
         print(err)    
