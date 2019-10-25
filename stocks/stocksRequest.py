from . import app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
import requests
from . import redis_store
import datetime
import json
import decimal


HOST = 'http://www.pse.com.ph/stockMarket/home.html'
HEADERS = {'Referer': HOST}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def insert_stocks():
    scheduler = BackgroundScheduler(executors=executors,job_defaults=job_defaults)
    scheduler.add_job(retrieve_stocks,CronTrigger.from_crontab('* * * * *'))
    scheduler.start()

def retrieve_stocks():
    print("Getting new stocks:" + str(datetime.datetime.now()))
    try:
        r = requests.get(HOST + '?method=getSecuritiesAndIndicesForPublic&ajax=true', headers=HEADERS, timeout=5)
        stocks = r.json()
        if len(stocks) !=  0:
            price_as_of = stocks[0]['securityAlias']
            for stock in stocks:
                stock['priceAsOf'] = price_as_of
                redis_store.set('stocks:' + stock['securitySymbol'], json.dumps(stock))
            stocks = json.dumps(stocks[1:])
            redis_store.set('stocks:all', stocks)
            winners = get_winners_or_losers(stocks,True)
            redis_store.set('stocks:top_gainers',json.dumps(winners))
            losers = get_winners_or_losers(stocks,False)
            redis_store.set('stocks:top_losers',json.dumps(losers))
            r = requests.get(HOST + '?method=getTopSecurity&limit=10&ajax=true', headers=HEADERS)
            active = (r.json()['records'])
            for stock in active:
                stock['priceAsOf'] = price_as_of
            redis_store.set('stocks:most_active', json.dumps(active).replace('lastTradePrice', 'lastTradedPrice'))
    except requests.exceptions.Timeout as err:
         print(err)    

#Sorting for top gainers and top losers
def get_winners_or_losers(stocks_data,flag):
    stocks = json.loads(stocks_data)
    sorted_data = sorted(stocks[1:],key=lambda x:decimal.Decimal(x['percChangeClose']),reverse=flag)
    return sorted_data[:10]