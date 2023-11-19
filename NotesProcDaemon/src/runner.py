from .services.message import Message
from .redis_client import r

from .db import database, crud


class Runner:
    _services = []
    _running = False

    def register_services(self, *services):
        self._services.extend(services)

    def run(self):
        self._running = True
        self._on_start()

        try:
            while self._running:
                message = self._read_message()
                print('Processing message:', message)
                self._dispense(message)
                print('Processed message:', message.id)
                self._set_last_message_id(message.id)
        finally:
            self._running = False
            self._on_stop()

    def _read_message(self) -> Message:
        messages = r.xread({
            'npd': self._get_last_message_id()
        }, count=1, block=0)[0][1]
        assert len(messages) == 1
        message = messages[0]
        return Message(message[0], message[1]['channel'], message[1])

    def _dispense(self, message):
        for service in self._services:
            service.process(message, message.channel)

    def _on_start(self):
        with database.SessionLocal() as session:
            crud.init_message_tracker(session)

        # todo: use logging as normal people do...
        print('\nNotes Processing Daemon is running\n')

    def _on_stop(self):
        pass

    def _get_last_message_id(self):
        with database.SessionLocal() as session:
            return crud.get_last_message_id(session)

    def _set_last_message_id(self, id: str):
        with database.SessionLocal() as session:
            return crud.set_last_message_id(session, id)



