from . import app
from .stock import Stock
from .response import Response
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