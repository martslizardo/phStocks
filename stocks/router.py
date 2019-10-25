from . import app
from .stock import Stock
from .stocksResponse import Response
from flask import jsonify


@app.route('/stocks')
def retrieve_all_stocks():
    stocks = Stock.getStocks("all")
    return jsonify(Response(stocks).__dict__)

@app.route('/stocks/<securitySymbol>')    
def get_stock(securitySymbol):
    stock = []
    stock = Stock.getStock(securitySymbol)
    return jsonify(Response(stock).__dict__)

@app.route('/stocks/winners')    
def winners():
    stock = Stock.getStocks("top_gainers")
    return jsonify(Response(stock).__dict__)    


@app.route('/stocks/losers')    
def losers():
    stock = Stock.getStocks("top_losers")
    return jsonify(Response(stock).__dict__)   \


@app.route('/stocks/active')    
def active():
    stock = Stock.getStocks("most_active")
    return jsonify(Response(stock).__dict__)   