from app.schemas.list import ListOut
from typing import List, Optional
from app.crud.types import NoteType
from pydantic import BaseModel


class NoteBase(BaseModel):
    name: str
    shared: bool
    type: NoteType
    text_body: str


class NoteUpdate(BaseModel):
    new_name: Optional[str]
    shared: Optional[bool]
    text_body: Optional[str]


class NoteCreate(NoteBase):
    pass


class NoteDb(NoteBase):
    id: int


class NoteOut(NoteDb):
    lists: List[ListOut]

    class Config:
        orm_mode = True
