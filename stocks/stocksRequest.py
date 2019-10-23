from . import app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
import requests
from . import redis_store
import datetime
import json


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
    except requests.exceptions.Timeout as err:
         print(err)    
