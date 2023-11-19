

class Message:
    id: str
    data: dict

    def __init__(self, id: str, channel: str, data: dict):
        self.id = id
        self.channel = channel
        self.data = data

    def __repr__(self):
        return f'Message({self.id}, {self.data})'
