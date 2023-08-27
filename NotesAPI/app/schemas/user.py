from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserRegister(UserBase):
    name: str
    password: str

class UserLogin(UserBase):
    password: str

