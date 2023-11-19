from ..message import Message
from ..service import BaseService
from ... import redis_client
from ... import api_util
from ... import models
from ...schemas import NoteCategory
from ...db import database
from ...db import crud
from ...lib import embeddings

import uuid


class Service(BaseService):
    def process(self, message: Message, channel):
        if channel != 'note_category':
            return

        if not message.data['uuid']:
            print('note_category_processor: uuid absent')
            return

        if not message.data['user_uuid']:
            print('note_category_processor: user_uuid absent')
            return

        try:
            category = api_util.get_note_category_by_uuid(message.data['uuid'])
        except Exception as e:
            print(e)
            return

        # get embedding
        note_category_embedding = self._get_category_embedding(category)

        # put embedding into db
        self._upsert_note_category_embedding(category.uuid, note_category_embedding)

        # categorize all notes of the user again
        self._recategorize_user_notes(message.data['user_uuid'])

    def _get_category_embedding(self, category: NoteCategory):
        ctx = embeddings.context.EmbeddingContext()
        ctx.strategy = embeddings.distilbert_strategy.DistilBertStrategy()

        embedding = ctx.encode([category.name])[0]

        return embedding

    def _upsert_note_category_embedding(self, note_category_uuid: str, embedding):
        with database.SessionLocal() as session:
            nce_obj = crud.cat_embeddings.get_note_embedding_by_note(session, note_category_uuid)
            if nce_obj is None:
                nce_obj = models.NoteCategoryEmbedding()
                nce_obj.uuid = uuid.uuid4()
                nce_obj.note_category_uuid = note_category_uuid
                nce_obj.embedding_768 = embedding
                nce_obj.version = '0.0b'

                crud.cat_embeddings.add_note_category_embedding(
                    session,
                    nce_obj
                )
            else:
                nce_obj.embedding_768 = embedding
            session.commit()

    def _recategorize_user_notes(self, user_uuid: str):
        note_uuids = api_util.get_note_uuids_by_user(user_uuid)
        for note_uuid in note_uuids:
            redis_client.r.xadd(
                name='npd',
                fields={
                    'channel': 'note',
                    'user_uuid': user_uuid,
                    'uuid': note_uuid
                }
            )


