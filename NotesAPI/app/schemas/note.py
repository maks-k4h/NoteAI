from pydantic import BaseModel
import uuid

from .category import BaseCategory, IdentifiedBaseCategory


class NoteBase(BaseModel):
    title: str | None = None
    content: str


class IdentifiedNote(NoteBase):
    uuid: str | uuid.UUID


class NoteWithCategories(NoteBase):
    categories: list[BaseCategory]


class IdentifiedNoteWithIdentifiedCategories(IdentifiedNote):
    categories: list[IdentifiedBaseCategory]

