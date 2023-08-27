import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import oauth2
from sqlalchemy.orm import Session
from ..db.crud import user as crud
from ..db.database import get_db_session
from ..models import User
from .password import verify
from .token import decode_token


oauth2_schema = oauth2.OAuth2PasswordBearer(tokenUrl='/account/token')


def authenticate_user(db_session: Session, email: str, password: str) -> User | None:
    user = crud.get_by_email(db_session, email)
    if not user:
        return None
    if not verify(password, user.password):
        return None
    return user


def get_current_user(session: Annotated[Session, Depends(get_db_session)], token: Annotated[str, Depends(oauth2_schema)]) -> User:
    try:
        print(token)
        payload = decode_token(token)
        uuid_str = payload.uuid
        return crud.get_by_uuid(session, uuid.UUID(uuid_str))
    except:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid authentication credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )

