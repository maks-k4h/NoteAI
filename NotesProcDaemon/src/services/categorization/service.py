from ..service import BaseService
from ... import api_util


class Service(BaseService):
    def process(self, message):
        if message.data['uuid']:
            note = api_util.get_note_by_uuid(message.data['uuid'])
            print(note)
