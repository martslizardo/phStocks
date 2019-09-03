from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__,instance_relative_config=True)


redis_store = FlaskRedis(app)

from .stocksRequest import retrieve_stocks

stocksRequest.retrieve_stocks()

from . import router
