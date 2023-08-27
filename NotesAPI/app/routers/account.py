import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi import Body, Depends
from fastapi.security import oauth2
from fastapi import Response, HTTPException, status

from ..schemas import user as user_models
from ..security import password as security_password, user as security_user, token as security_token

from .. import models
from ..db.database import get_db_session, Session
from ..db.crud import user as user_crud

import uuid


router = APIRouter(
    prefix='/account',
    tags=['Account'],
)


@router.get('/')
def get_account_info(user: Annotated[models.User, Depends(security_user.get_current_user)]):
    return user


@router.post('/register')
def register_user(session: Annotated[Session, Depends(get_db_session)], user: user_models.UserRegister):
    if user_crud.check_email(session, user.email):
        return HTTPException(status.HTTP_400_BAD_REQUEST, 'This email is already used.')
    if user_crud.check_name(session, user.name):
        return HTTPException(status.HTTP_400_BAD_REQUEST, 'This name is already used.')

    # add new user
    db_user = models.User()
    db_user.uuid = uuid.uuid4()
    db_user.email = user.email
    db_user.password = security_password.get_hash(user.password)

    db_usermeta = models.UserMeta()
    db_usermeta.name = user.name

    db_user.user_meta = db_usermeta

    if not user_crud.put_user(session, db_user):
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_200_OK)


@router.post('/token')
def get_token(session: Annotated[Session, Depends(get_db_session)],
              form_data: Annotated[oauth2.OAuth2PasswordRequestForm, Depends()]):

    user = security_user.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, 'Wrong credentials')

    token_data = security_token.TokenData(uuid=str(user.uuid))
    token = security_token.create_token(token_data.dict(), datetime.timedelta(minutes=30))
    return token



