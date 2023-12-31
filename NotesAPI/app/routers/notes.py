from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi import Response, status

from .. import security

from ..db.database import get_db_session, Session
from ..db import crud
from .. import models

from .. import schemas

from ..events import note as events_note

import uuid


router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)


@router.get(
    '/',
    response_model=list[schemas.note.IdentifiedNote]
)
def get_notes(db_session: Annotated[Session, Depends(get_db_session)],
              user_uuid: Annotated[str, Depends(security.user.get_current_user_uuid)],
              offset: Annotated[int, Query(ge=0)] = 0,
              limit: Annotated[int | None, Query(ge=0)] = None,
              user_uuid_filter: str | None = None   # get notes of other user (used by other services)
):
    if user_uuid_filter and not security.roles.authorize_uuid(user_uuid, security.roles.NPDAEMON):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Unauthorized to use user_uuid_filter')

    if not user_uuid_filter:
        notes = crud.note.get_by_user_uuid(db_session, uuid.UUID(user_uuid), offset, limit)
    else:
        notes = crud.note.get_by_user_uuid(db_session, uuid.UUID(user_uuid_filter), offset, limit)

    return notes


@router.get(
    '/detailed',
    response_model=list[schemas.note.IdentifiedNoteWithIdentifiedCategories]
)
def get_notes_detailed(db_session: Annotated[Session, Depends(get_db_session)],
              user_uuid: Annotated[str, Depends(security.user.get_current_user_uuid)],
              offset: Annotated[int, Query(ge=0)] = 0,
              limit: Annotated[int | None, Query(ge=0)] = None,
              user_uuid_filter: str | None = None   # get notes of other user (used by other services)
):
    if user_uuid_filter and not security.roles.authorize_uuid(user_uuid, security.roles.NPDAEMON):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Unauthorized to use user_uuid_filter')

    if not user_uuid_filter:
        notes = crud.note.get_by_user_uuid(db_session, uuid.UUID(user_uuid), offset, limit)
    else:
        notes = crud.note.get_by_user_uuid(db_session, uuid.UUID(user_uuid_filter), offset, limit)

    return notes


@router.get(
    '/{note_uuid}',
    response_model=schemas.note.NoteBase
)
def get_note(
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security.user.get_current_user_uuid)],
        note_uuid: str
):
    # retrieve uuid
    try:
        note_uuid = uuid.UUID(note_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = crud.note.get_by_uuid(db_session, note_uuid)

    if not note or (note.user_uuid.__str__() != user_uuid
                    and not security.roles.authorize_uuid(user_uuid, security.roles.NPDAEMON)):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return note


@router.get(
    '/{note_uuid}/details',
    response_model=schemas.note.IdentifiedNoteWithIdentifiedCategories
)
def get_note_details(
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security.user.get_current_user_uuid)],
        note_uuid: str
):
    # retrieve uuid
    try:
        note_uuid = uuid.UUID(note_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = crud.note.get_by_uuid(db_session, note_uuid)

    if not note or note.user_uuid.__str__() != user_uuid:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return note


@router.get(
    '/{note_uuid}/categories',
    response_model=list[schemas.category.IdentifiedBaseCategory]
)
def get_note_categories(
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security.user.get_current_user_uuid)],
        note_uuid: str
):
    # retrieve uuid
    try:
        note_uuid = uuid.UUID(note_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = crud.note.get_by_uuid(db_session, note_uuid)

    if not note or note.user_uuid.__str__() != user_uuid:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    categories = note.categories

    return categories


@router.post(
    '/{note_uuid}/categories/add'
)
def add_note_category(
        db_session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[models.User, Depends(security.user.get_current_user)],
        note_uuid: str,
        category_uuid: str,
):
    # retrieve uuid
    try:
        note_uuid = uuid.UUID(note_uuid)
        category_uuid = uuid.UUID(category_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = crud.note.get_by_uuid(db_session, note_uuid)
    category = crud.category.get_by_uuid(db_session, category_uuid)

    if (not note or (note.user_uuid != user.uuid and
                     not security.roles.authorize_uuid(str(user.uuid), security.roles.NPDAEMON))):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Note not found')

    if (not category or (category not in user.categories
                         and not security.roles.authorize_uuid(str(user.uuid), security.roles.NPDAEMON))):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category not found')

    if category in note.categories:
        return Response(status_code=status.HTTP_200_OK, content='The category is already associated with the note')

    note.categories.append(category)
    db_session.commit()

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    '/{note_uuid}/categories/delete'
)
def remove_note_category(
        db_session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[models.User, Depends(security.user.get_current_user)],
        note_uuid: str,
        category_uuid: str,
):
    # retrieve uuid
    try:
        note_uuid = uuid.UUID(note_uuid)
        category_uuid = uuid.UUID(category_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = crud.note.get_by_uuid(db_session, note_uuid)
    category = crud.category.get_by_uuid(db_session, category_uuid)

    if (not note
            or note.user_uuid != user.uuid):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Note not found')

    if (not category
            or category not in user.categories):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category not found')

    if category not in note.categories:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'The category is not assigned to this note')

    note.categories.remove(category)
    db_session.commit()

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    '/{note_uuid}/categories/delete/all'
)
def remove_note_category(
        db_session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[models.User, Depends(security.user.get_current_user)],
        note_uuid: str,
):
    # retrieve uuid
    try:
        note_uuid = uuid.UUID(note_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = crud.note.get_by_uuid(db_session, note_uuid)

    if (not note or (note.user_uuid != user.uuid and
                     not security.roles.authorize_uuid(str(user.uuid), security.roles.NPDAEMON))):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Note not found')

    categories = list(note.categories)
    for category in categories:
        note.categories.remove(category)
    db_session.commit()

    return Response(status_code=status.HTTP_200_OK)


@router.post(
    '/create',
)
async def create_note(db_session: Annotated[Session, Depends(get_db_session)],
                user_uuid: Annotated[str, Depends(security.user.get_current_user_uuid)],
                note: schemas.note.NoteBase):

    db_note = models.Note()
    db_note.uuid = uuid.uuid4()
    db_note.user_uuid = uuid.UUID(user_uuid)
    db_note.title = note.title
    db_note.content = note.content

    if not crud.note.put_note(db_session, db_note):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # log the event
    events_note.log_content_change(db_note.uuid.__str__(), user_uuid)

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    '/delete'
)
def delete_note(db_session: Annotated[Session, Depends(get_db_session)],
                user_uuid: Annotated[str, Depends(security.user.get_current_user_uuid)],
                note_uuid: str):

    try:
        note_uuid = uuid.UUID(note_uuid)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid UUID')

    note = crud.note.get_by_uuid(db_session, note_uuid)

    if not note or not note.user_uuid.__str__() == user_uuid:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Note not found')

    if not crud.note.delete(db_session, note):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_200_OK)



