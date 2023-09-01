from pydantic import BaseModel

from uuid import UUID


class BaseCategory(BaseModel):
    name: str


class IdentifiedBaseCategory(BaseCategory):
    uuid: str | UUID


class UserCategory(BaseCategory):
    user_uuid: str | UUID



