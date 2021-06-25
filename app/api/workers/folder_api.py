from app.context.auth_context import AppContextAuth
from app.crud.models import Folder
from app.api.workers.note_api import NoteApi
from app.crud.note import NoteDb
from app.crud.user import UserDb
from typing import List
from app.crud.folder import FolderDb
from app.schemas.folder import FolderCreate, FolderOut, FolderUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class FolderApi:
    ctx: AppContextAuth
    db: Session
    user_db: UserDb
    folder_db: FolderDb
    note_db: NoteDb

    def __init__(self, context: AppContextAuth):
        self.ctx = context
        self.db = context.db
        self.user_db = UserDb(context)
        self.folder_db = FolderDb(context)
        self.note_db = NoteDb(context)
        self.note_api = NoteApi(context)

    def create(self, user_id: str, folder: FolderCreate) -> FolderOut:
        self.__validate_user__(user_id)
        self.__check_foldername_not_exist__(user_id, folder.name)

        folder_db = self.folder_db.create(user_id, folder)
        return self._map_folder(folder_db)

    def update(self, user_id: int, folder_id: int, folder_update: FolderUpdate) -> FolderOut:
        self.__validate_user__(user_id)
        return self.folder_db.update(folder_id, folder_update)

    def delete(self, user_id: int, folder_id: int, force: bool):
        self.__validate_user__(user_id)

        folder = self.get(folder_id)
        folder_notes = self.note_db.get_all(folder.id)
        if len(folder_notes) > 0 and not force:
            self.__raise_nonempty_folder__(folder.id)
        for note in folder_notes:
            self.note_api.delete(note.id)

        self.folder_db.delete(folder.id)

    def get_all_default(self) -> List[FolderOut]:
        folders_db = self.folder_db.get_all()
        return list(map(lambda f: self._map_folder(f), folders_db))

    def get_all(self, user_id: int) -> List[FolderOut]:
        folders_db = self.folder_db.get_all_for_id(user_id)
        return list(map(lambda f: self._map_folder(f), folders_db))

    def get(self, user_id, folder_id: int) -> FolderOut:
        folder_db = self.folder_db.get(folder_id)
        return self._map_folder(folder_db)

    def get_by_name(self, user_id: int, name: str) -> FolderOut:
        self.__check_foldername_exist__(user_id, name)
        folder_db = self.folder_db.get_by_name(user_id, name)
        return self._map_folder(folder_db)

    def _map_folder(self, folder_db: Folder) -> FolderOut:
        return FolderOut(**vars(folder_db), notes=self.note_api.get_all(folder_db.id))

    def __validate_user__(self, user_id: int):
        if self.ctx.user.id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Logged user and queried user do not match!")

    def __check_foldername_exist__(self, user_id: int, name: str):
        if not self.folder_db.folder_exists(user_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Folder with name '{name}' doesn't exist")

    def __check_foldername_not_exist__(self, user_id: int, name: str):
        if self.folder_db.folder_exists(user_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Folder with name '{name}' already exists")

    def __raise_nonempty_folder__(self, folder_id: int):
        msg = f"""
            Folder with id {folder_id} cannot be deleted since it has nested notes.
            If you wish to recursively delete nested notes, rerequest api with parameter force=true.
        """
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, msg)
