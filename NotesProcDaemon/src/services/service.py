from .message import Message


class BaseService:
    def process(self, message: Message, channel: str):
        """

        :param message:
        :param channel: depending on the channel, processing may be declined
        :return:
        """
        raise NotImplementedError()
