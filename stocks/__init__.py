from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__,instance_relative_config=True)


redis_store = FlaskRedis(app)

from .ticker import retrieve_stocks

ticker.retrieve_stocks()

from . import router
