from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi import Response, status

from ..security import user as security_user

from ..db.database import get_db_session, Session
from ..db.crud import note as notes_crud
from .. import models

from ..schemas import note as schema_note

from ..events import note as events_note

import uuid


router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)


@router.get(
    '/',
    response_model=list[schema_note.IdentifiedNote]
)
def get_notes(db_session: Annotated[Session, Depends(get_db_session)],
              user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
              offset: Annotated[int, Query(ge=0)] = 0,
              limit: Annotated[int | None, Query(ge=0)] = None
):

    notes = notes_crud.get_by_user_uuid(db_session, uuid.UUID(user_uuid), offset, limit)

    return notes


@router.get(
    '/details/{note_uuid}',
    response_model=schema_note.IdentifiedNoteWithIdentifiedCategories
)
def get_note_details(
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[models.User, Depends(security_user.get_current_user_uuid)],
        note_uuid: str
):
    # retrieve uuid
    try:
        note_uuid = uuid.UUID(note_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = notes_crud.get_by_uuid(db_session, note_uuid)

    if not note or note.user_uuid.__str__() != user_uuid:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return note


@router.post(
    '/create',
)
async def create_note(db_session: Annotated[Session, Depends(get_db_session)],
                user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
                note: schema_note.NoteBase):

    db_note = models.Note()
    db_note.uuid = uuid.uuid4()
    db_note.user_uuid = uuid.UUID(user_uuid)
    db_note.title = note.title
    db_note.content = note.content

    if not notes_crud.put_note(db_session, db_note):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # log the event
    events_note.log_content_change(db_note.uuid.__str__())

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    '/delete'
)
def delete_note(db_session: Annotated[Session, Depends(get_db_session)],
                user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
                note_uuid: str):

    try:
        note_uuid = uuid.UUID(note_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = notes_crud.get_by_uuid(db_session, note_uuid)

    if not note or not note.user_uuid.__str__() == user_uuid:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Note not found')

    if not notes_crud.delete(db_session, note):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_200_OK)








