from pydantic import BaseModel
import uuid


class NoteBase(BaseModel):
    title: str | None = None
    content: str


class IdentifiedNote(NoteBase):
    uuid: str | uuid.UUID

