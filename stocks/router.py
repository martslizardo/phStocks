from . import app
from .stock import Stock
from .response import Response
from flask import jsonify


@app.route('/stocks')
def retrieve_all_stocks():
    stocks = Stock.getStocks("all")
    return jsonify(Response("OK", stocks).__dict__)