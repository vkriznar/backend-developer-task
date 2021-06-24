from app.crud.folder import FolderDb
from app.context.auth_context import AppContextAuth
from app.crud.models import Note
from app.api.workers.list_api import ListApi
from app.crud.list import ListDb
from app.crud.types import HeadingSort, NoteType, SharedType
from app.crud.user import UserDb
from typing import List
from app.crud.note import NoteDb
from app.schemas.note import NoteCreate, NoteOut, NoteUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class NoteApi:
    ctx: AppContextAuth
    db: Session
    user_db: UserDb
    note_db: NoteDb
    list_db: ListDb

    def __init__(self, context: AppContextAuth):
        self.ctx = context
        self.db = context.db
        self.folder_db = FolderDb(context)
        self.user_db = UserDb(context)
        self.note_db = NoteDb(context)
        self.list_db = ListDb(context)
        self.list_api = ListApi(context)

    def create(self, user_id: int, folder_id: int, note: NoteCreate) -> NoteOut:
        self.__validate_user__(user_id)
        self.__check_notename_not_exist__(folder_id, note.name)
        self._check_note_validity(note.type, note.text_body)

        note_db = self.note_db.create(folder_id, note)
        return self._map_note(note_db)

    def update(self, user_id: int, note_id: int, note_update: NoteUpdate) -> NoteOut:
        self.__validate_user__(user_id)
        if note_update.text_body is not None:
            note = self.note_db.get(note_id)
            self._check_note_validity(note.type, note_update.text_body)
        return self.note_db.update(note_id, note_update)

    def delete(self, user_id: int, note_id: int, force: bool):
        self.__validate_user__(user_id)
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

        filtered_notes = filter(lambda n: self._filter_by_user(n, self.ctx.user.id), notes_db)
        return list(map(lambda n: self._map_note(n), filtered_notes))

    def get_all_default(
        self,
        folder_id: int,
        notes_per_page: int,
        page_nr: int,
        shared_filter: SharedType,
        node_text_filter: str,
        shared_sorting: SharedType,
        heading_sorting: HeadingSort
    ) -> List[NoteOut]:

        notes_db = self.note_db.get_all() if folder_id is None else self.note_db.get_all_for_id(folder_id)

        # Filter those that can be seen by logged in user
        logged_user_id = self.ctx.user.id if hasattr(self.ctx, "user") else -2
        notes = filter(lambda n: self._filter_by_user(n, logged_user_id), notes_db)

        # Filter by public/private parameter
        if shared_filter != SharedType.NONE:
            notes = filter(lambda n: n.shared if shared_filter == SharedType.PUBLIC else not n.shared, notes)

        notes = map(lambda n: self._map_note(n), notes)

        # Filter by text value
        if node_text_filter is not None:
            notes = filter(lambda n: self._filter_by_text(n, node_text_filter), notes)

        # Sort by shared/public parameter
        if shared_sorting != SharedType.NONE:
            notes = sorted(notes, key=lambda n: n.shared, reverse=(shared_sorting == SharedType.PUBLIC))

        # Sort by heading (name) of note
        if heading_sorting is not HeadingSort.NONE:
            notes = sorted(notes, key=lambda n: n.name, reverse=(heading_sorting == HeadingSort.DESCENDING))

        # Do pagination
        final_notes = list(notes)
        notes = [final_notes[i:i + notes_per_page] for i in range(0, len(list(final_notes)), notes_per_page)]

        if len(notes) < page_nr:
            return []
        return notes[page_nr-1]

    def get(self, user_id: int, note_id: int) -> NoteOut:
        note_db = self.note_db.get(note_id)
        if not note_db.shared:
            self.__validate_user__(user_id)
        return self._map_note(note_db)

    def get_by_name(self, user_id: int, folder_id: int, name: str) -> NoteOut:
        self.__check_notename_exist__(folder_id, name)
        note_db = self.note_db.get_by_name(folder_id, name)
        return self._map_note(note_db)

    def _filter_by_user(self, note: Note, logged_user_id: int) -> bool:
        folder = self.folder_db.get(note.folder_id)
        return note.shared or logged_user_id == folder.user_id

    def _map_note(self, note_db: Note) -> NoteOut:
        return NoteOut(**vars(note_db), lists=self.list_api.get_all(note_db.id))

    def _filter_by_text(self, note: NoteOut, text: str):
        if note.type == NoteType.TEXT:
            return text in note.text_body
        for list in note.lists:
            if text in list.text_body:
                return True
        return False

    def _check_note_validity(self, type: NoteType, text_body: str):
        if type == NoteType.LIST and text_body is not None:
            self.__raise_nonempty_text_body__()
        elif type == NoteType.TEXT and text_body is None:
            self.__raise_empty_text_body__()

    def __validate_user__(self, user_id: int):
        if self.ctx.user.id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Logged user and queried user do not match!")

    def __check_notename_exist__(self, folder_id: int, name: str):
        if not self.note_db.note_exists(folder_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Note with name '{name}' doesn't exist")

    def __check_notename_not_exist__(self, folder_id: int, name: str):
        if self.note_db.note_exists(folder_id, name):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Note with name '{name}' already exists")

    def __raise_nonempty_note__(self, note_id: int):
        msg = f"Note with id {note_id} cannot be deleted since it has nested lists. If you wish to recursively delete nested lists, re-request api with parameter force=true."
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, msg)

    def __raise_nonempty_text_body__(self):
        msg = f"Cannot create/update note, since it has type {NoteType.LIST} therefore it cannot have non-empty text_body field."
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, msg)

    def __raise_empty_text_body__(self):
        msg = f"Cannot create/update note, since it has type {NoteType.TEXT} therefore it cannot have empty text_body field."
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, msg)
