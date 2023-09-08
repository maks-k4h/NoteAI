from services.message import Message
from redis_client import r

class Runner:
    _services = []

    def register_services(self, *services):
        self._services.extend(services)

    def run(self):
        for i in range(5):
            message = self._read_message()
            self._dispense(message)

    def _read_message(self) -> Message:
        messages = r.xread({
            'changes:notes': '$'
        }, count=1, block=0)[0][1]
        assert len(messages) == 1
        message = messages[0]
        return Message(message[0], message[1])

    def _dispense(self, message):
        for service in self._services:
            service.process(message)
