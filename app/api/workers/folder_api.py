from app.crud.user import UserDb
from typing import List
from app.crud.folder import FolderDb
from app.schemas.folder import FolderCreate, FolderOut, FolderUpdate
from sqlalchemy.orm import Session
from app.context.context import AppContext
from fastapi import HTTPException, status


class FolderApi:
    db: Session

    def __init__(self, context: AppContext):
        self.db = context.db
        self.user_db = UserDb(context)
        self.folder_db = FolderDb(context)

    def __check_foldername_exist__(self, user_id: int, name: str):
        if not self.folder_db.folder_exists(user_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Folder with name '{name}' doesn't exist")

    def __check_foldername_not_exist__(self, user_id: int, name: str):
        if self.folder_db.folder_exists(user_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Folder with name '{name}' already exists")

    def create(self, user_id: str, folder: FolderCreate) -> FolderOut:
        self.__check_foldername_not_exist__(user_id, folder.name)
        return self.folder_db.create(user_id, folder)

    def update(self, folder_id: int, folder_update: FolderUpdate) -> FolderOut:
        return self.folder_db.update(folder_id, folder_update)

    def delete(self, folder_id: int, force: bool):
        # Implement first api for notes and lists
        pass

    def get_all(self, user_id: str) -> List[FolderOut]:
        return self.folder_db.get_all(user_id)

    def get(self, folder_id: int) -> FolderOut:
        return self.folder_db.get(folder_id)

    def get_by_name(self, user_id: str, name: str) -> FolderOut:
        self.__check_foldername_exist__(user_id, name)
        return self.folder_db.get_by_name(user_id, name)
