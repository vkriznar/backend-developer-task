from app.crud.models import Note
from app.api.workers.list_api import ListApi
from app.crud.list import ListDb
from app.crud.types import NoteType
from app.crud.user import UserDb
from typing import List
from app.crud.note import NoteDb
from app.schemas.note import NoteBase, NoteCreate, NoteOut, NoteUpdate
from sqlalchemy.orm import Session
from app.context.context import AppContext
from fastapi import HTTPException, status


class NoteApi:
    db: Session
    user_db: UserDb
    note_db: NoteDb
    list_db: ListDb

    def __init__(self, context: AppContext):
        self.db = context.db
        self.user_db = UserDb(context)
        self.note_db = NoteDb(context)
        self.list_db = ListDb(context)
        self.list_api = ListApi(context)

    def __check_notename_exist__(self, folder_id: int, name: str):
        if not self.note_db.note_exists(folder_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Note with name '{name}' doesn't exist")

    def __check_notename_not_exist__(self, folder_id: int, name: str):
        if self.note_db.note_exists(folder_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Note with name '{name}' already exists")

    def __raise_nonempty_note__(self, note_id: int):
        msg = f"Note with id {note_id} cannot be deleted since it has nested lists. If you wish to recursively delete nested lists, rerequest api with parameter force=true."
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, msg)

    def __raise_nonempty_text_body__(self):
        msg = f"Cannot create/update note, since it has type {NoteType.LIST} therefore it cannot have non-empty text_body field."
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, msg)

    def __raise_empty_text_body__(self):
        msg = f"Cannot create/update note, since it has type {NoteType.TEXT} therefore it cannot have empty text_body field."
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, msg)

    def create(self, folder_id: int, note: NoteCreate) -> NoteOut:
        self.__check_notename_not_exist__(folder_id, note.name)
        self._check_note_validity(note.type, note.text_body)

        note_db = self.note_db.create(folder_id, note)
        return self._map_note(note_db)

    def update(self, note_id: int, note_update: NoteUpdate) -> NoteOut:
        if note_update.text_body is not None:
            note = self.note_db.get(note_id)
            self._check_note_validity(note.type, note_update.text_body)
        return self.note_db.update(note_id, note_update)

    def delete(self, note_id: int, force: bool):
        note = self.get(note_id)
        if note.type == NoteType.LIST:
            note_lists = self.list_db.get_all(note.id)
            if len(note_lists) > 0 and not force:
                self.__raise_nonempty_note__(note.id)
            for list in note_lists:
                self.list_db.delete(list.id)

        self.note_db.delete(note_id)

    def get_all(self, folder_id: int) -> List[NoteOut]:
        notes_db = self.note_db.get_all(folder_id)
        return list(map(lambda n: self._map_note(n), notes_db))

    def get(self, note_id: int) -> NoteOut:
        note_db = self.note_db.get(note_id)
        return self._map_note(note_db)

    def get_by_name(self, folder_id: int, name: str) -> NoteOut:
        self.__check_notename_exist__(folder_id, name)
        note_db = self.note_db.get_by_name(folder_id, name)
        return self._map_note(note_db)

    def _map_note(self, note_db: Note) -> NoteOut:
        return NoteOut(**vars(note_db), lists=self.list_api.get_all(note_db.id))

    def _check_note_validity(self, type: NoteType, text_body: str):
        if type == NoteType.LIST and text_body is not None:
            self.__raise_nonempty_text_body__()
        elif type == NoteType.TEXT and text_body is None:
            self.__raise_empty_text_body__()
