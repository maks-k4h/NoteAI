

class Message:
    id: str
    data: dict

    def __init__(self, id: str, data: dict):
        self.id = id
        self.data = data

    def __repr__(self):
        return f'Message({self.id}, {self.data})'
