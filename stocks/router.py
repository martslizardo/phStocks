from . import app
from .ticker import retrieve_stocks
import sys

sys.setrecursionlimit(15000)
stocks = retrieve_stocks()
@app.route('/stocks')
def retrieve_stocks():
    return stocks