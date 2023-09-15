import os

from datetime import timedelta, datetime

from pydantic import BaseModel
from fastapi import HTTPException, status

from jose import JWTError, jwt


SIGNATURE = os.environ['SIGNATURE']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uuid: str


def create_token(data: dict, expires_delta: timedelta | None = None) -> Token:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SIGNATURE, algorithm=JWT_ALGORITHM)
    return Token(access_token=encoded_jwt, token_type='bearer')


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SIGNATURE, JWT_ALGORITHM)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return TokenData(uuid=payload['uuid'])
