from .message import Message


class BaseService:
    def process(self, message: Message):
        raise NotImplementedError()
