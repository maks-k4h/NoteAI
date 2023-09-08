from ..service import BaseService


class Service(BaseService):
    def process(self, message):
        print('Processing message:', message)

