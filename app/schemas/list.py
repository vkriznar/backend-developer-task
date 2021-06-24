from pydantic import BaseModel


class ListBase(BaseModel):
    text_body: str


class ListUpdate(ListBase):
    pass


class ListCreate(ListBase):
    pass


class ListDbSchema(ListBase):
    id: int


class ListOut(ListDbSchema):
    pass

    class Config:
        orm_mode = True
