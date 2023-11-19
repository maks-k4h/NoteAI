import uuid
import datetime

from pydantic import BaseModel


class ImageMetadata(BaseModel):
    uuid: str | uuid.UUID
    user_uuid: str | uuid.UUID
    added: datetime.datetime
    deleted: datetime.datetime | None = None
    location: str | None = None
    path: str
    size: int | None = None
