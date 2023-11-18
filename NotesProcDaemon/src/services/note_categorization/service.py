import uuid

from ..service import BaseService
from ... import api_util
from ...schemas import Note
from ...db import database
from ...db import crud
from ...lib import embeddings
from ... import models


class Service(BaseService):
    def process(self, message, channel) -> None:
        if channel != 'note':
            return

        if not message.data['uuid']:
            return

        try:
            note = api_util.get_note_by_uuid(message.data['uuid'])
        except Exception as e:
            print(e)
            return

        note_embedding = self._get_note_embedding(note)

        self._upsert_note_embedding(note.uuid, note_embedding)



    def _get_note_embedding(self, note: Note):
        ctx = embeddings.context.EmbeddingContext()
        ctx.strategy = embeddings.distilbert_strategy.DistilBertStrategy()

        embedding = ctx.encode([note.content])[0]

        return embedding

    def _upsert_note_embedding(self, note_uuid: str, embedding):
        with database.SessionLocal() as session:
            ne_obj = crud.cat_embeddings.get_note_embedding_by_note(session, note_uuid)
            if ne_obj is None:
                ne_obj = models.NoteEmbedding()
                ne_obj.uuid = uuid.uuid4()
                ne_obj.note_uuid = note_uuid
                ne_obj.embedding_768 = embedding
                ne_obj.version = '0.0b'

                crud.cat_embeddings.add_note_embedding(
                    session,
                    ne_obj
                )
            else:
                ne_obj.embedding_768 = embedding
            session.commit()


