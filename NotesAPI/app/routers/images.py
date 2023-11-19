import datetime
import uuid

from starlette.responses import Response

from .. import models
from ..security import user as security_user
from ..schemas.image import ImageMetadata
from ..db import crud
from ..db.database import get_db_session, Session

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from typing import Annotated


router = APIRouter(
    prefix='/images',
    tags=['Images']
)


@router.get(
    '/all/metadata',
    response_model=list[ImageMetadata],
)
def get_all_images_metadata(
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
):
    user_uuid = uuid.UUID(user_uuid)

    images = crud.image.get_images_by_user_uuid(db_session, user_uuid)
    return images


@router.get(
    '/archived/metadata',
    response_model=list[ImageMetadata],
)
def get_all_images_metadata(
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
):
    user_uuid = uuid.UUID(user_uuid)

    images = crud.image.get_deleted_images_by_user_uuid(db_session, user_uuid)
    return images


@router.get(
    '/{image_uuid}/metadata',
    response_model=ImageMetadata,
)
def get_all_images_metadata(
        image_uuid: str,
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
):
    try:
        image_uuid = uuid.UUID(image_uuid)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid uuid.')

    image = crud.image.get_by_uuid(db_session, image_uuid)

    if image is None or str(image.user_uuid) != user_uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if image.deleted is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This images is archived.')

    return image


@router.post(
    '/create',
    response_model=ImageMetadata
)
def add_image(
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
        image: UploadFile = File(...)
):
    try:
        # contents = image.file.read()
        size = image.size
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="There was an error uploading the image")
    finally:
        image.file.close()

    image = models.Image()
    image.uuid = str(uuid.uuid4())
    image.user_uuid = str(user_uuid)
    image.added = datetime.datetime.now()
    image.location = 'test'
    image.path = 'undefined'
    image.size = size

    db_session.add(image)
    db_session.commit()

    return image


@router.post(
    '/{image_uuid}/put_back'
)
def delete_image(
        image_uuid: str,
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
):
    try:
        image_uuid = uuid.UUID(image_uuid)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid uuid.')

    image = crud.image.get_by_uuid(db_session, image_uuid)

    if image is None or str(image.user_uuid) != user_uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if image.deleted is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The image is not archived')

    image.deleted = None
    db_session.commit()

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    '/{image_uuid}'
)
def delete_image(
        image_uuid: str,
        db_session: Annotated[Session, Depends(get_db_session)],
        user_uuid: Annotated[str, Depends(security_user.get_current_user_uuid)],
):
    try:
        image_uuid = uuid.UUID(image_uuid)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid uuid.')

    image = crud.image.get_by_uuid(db_session, image_uuid)

    if image is None or str(image.user_uuid) != user_uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if image.deleted is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The image is already archived')

    image.deleted = datetime.datetime.now()
    db_session.commit()

    return Response(status_code=status.HTTP_200_OK)



