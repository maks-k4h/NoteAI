import os

from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hash(password) -> str:
    return pwd_ctx.hash(password)


def verify(plain, hashed) -> bool:
    return pwd_ctx.verify(plain, hashed)
