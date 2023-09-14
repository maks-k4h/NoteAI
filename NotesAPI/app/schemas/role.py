import uuid

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: str | None = None


class IdentifiedRole(RoleBase):
    uuid: str

