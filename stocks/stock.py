from . import redis_store
import json

class Stock:
    def __init__(self,securitySymbol,price,dayChange,priceAsOf):
        self.securitySymbol = securitySymbol
        self.price = price
        self.dayChange = dayChange
        self.priceAsOf = priceAsOf

    def getStocks(key):
        stocks = []
        data = redis_store.get('stocks:' + key)
        if data is not None:
            data = json.loads(data)
            for stock in data:
                s = Stock(stock['securitySymbol'], stock['lastTradedPrice'], str(stock['percChangeClose']) + '%', stock['priceAsOf']) 
                stocks.append(s.serialize())
        return stocks        
    def getStock(key):
        stocks = []
        data = redis_store.get('stocks:'+ key)
        if data is not None:
            stock = json.loads(data)
            stock = Stock(stock['securitySymbol'], stock['lastTradedPrice'], str(stock['percChangeClose']) + '%', stock['priceAsOf']) 
            stocks.append(stock.serialize())
            print(json.dumps(stocks))
        return stocks

    def serialize(self):
        return {
            'securitySymbol': self.securitySymbol,
            'price': self.price,
            'dayChange': self.dayChange,
            'priceAsOf':self.priceAsOf
        }