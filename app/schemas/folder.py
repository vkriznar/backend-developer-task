from pydantic import BaseModel


class FolderBase(BaseModel):
    name: str


class FolderUpdate(BaseModel):
    new_name: str


class FolderCreate(FolderBase):
    pass


class FolderDb(FolderBase):
    id: int


class FolderOut(FolderDb):
    pass

    class Config:
        orm_mode = True
