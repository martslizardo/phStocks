
import json


class Response:
    def __init__(self, stocks):
        self.stocks = stocks

    def to_Json(self):
        return self.__dict__