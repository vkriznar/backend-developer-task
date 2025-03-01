from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    username: str


class UserCreate(UserBase):
    password: str


class UserDb(UserBase):
    id: int


class UserOut(UserDb):
    pass

    class Config:
        orm_mode = True
