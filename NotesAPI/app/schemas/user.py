from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserRegister(UserBase):
    email: str
    password: str


class UserLogin(UserBase):
    password: str

