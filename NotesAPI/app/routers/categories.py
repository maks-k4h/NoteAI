from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi import Response, status

from ..security import user as security_user

from ..db.database import get_db_session, Session
from ..db.crud import category as categories_crud
from .. import models

from ..schemas import category as schema_category

import uuid


router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)


@router.get(
    '/',
    response_model=list[schema_category.IdentifiedBaseCategory]
)
def get_categories(
        db_session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[models.User, Depends(security_user.get_current_user)],
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int | None, Query(ge=0)] = None):

    if limit is not None:
        user_categories = user.categories[offset:offset+limit]
    else:
        user_categories = user.categories[offset:]

    return user_categories


@router.post(
    '/create',
    response_model=schema_category.IdentifiedBaseCategory
)
def create_category(
        db_session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[models.User, Depends(security_user.get_current_user)],
        category_name: Annotated[str, Query(min_length=3)]):

    if not categories_crud.get_by_name(db_session, category_name):
        # category with this name doesn't exist
        db_category = models.Category()
        db_category.uuid = uuid.uuid4()
        db_category.name = category_name

        if not categories_crud.put_category(db_session, db_category):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Cannot create this category')

    db_category = categories_crud.get_by_name(db_session, category_name)

    # check if user already has this category
    if db_category in user.categories:
        raise HTTPException(status.HTTP_409_CONFLICT, 'The category is already connected to the user')

    # connect this user to the category
    db_category.users.append(user)
    db_session.commit()

    return db_category


@router.delete(
    '/remove',
    summary="Unlink user from the category",
    description="Unlinks category provided its uuid or name. If both are provided uuid will be used."
)
def unlink_category(
        db_session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[models.User, Depends(security_user.get_current_user)],
        category_uuid: str | None = None,
        category_name: str | None = None,
):

    if not (category_uuid or category_name):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Provide category\'s uuid or name')

    # retrieve category's uuid
    if not category_uuid:
        category = categories_crud.get_by_name(db_session, category_name)
        if not category:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category not found')
        category_uuid = category.uuid
    else:
        try:
            category_uuid = uuid.UUID(category_uuid)
        except:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid uuid')

    # disconnect the category
    if not categories_crud.disconnect_user(db_session, category_uuid, user):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Cannot disconnect user for the category')

    # todo: if it was the last usage remove the category too

    return Response(status_code=status.HTTP_200_OK)








