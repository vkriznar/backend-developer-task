from typing import List
from app.schemas.note import NoteOut
from pydantic import BaseModel


class FolderBase(BaseModel):
    name: str


class FolderUpdate(FolderBase):
    pass


class FolderCreate(FolderBase):
    pass


class FolderDb(FolderBase):
    id: int


class FolderOut(FolderDb):
    notes: List[NoteOut]

    class Config:
        orm_mode = True
