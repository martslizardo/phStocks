
import json


class Response:
    def __init__(self, status, data):
        self.status = status
        self.data = data

    def to_Json(self):
        return self.__dict__