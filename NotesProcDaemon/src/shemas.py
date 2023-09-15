from pydantic import BaseModel


class Note(BaseModel):
    uuid: str
    name: str | None
    content: str


class Category(BaseModel):
    uuid: str
    name: str



