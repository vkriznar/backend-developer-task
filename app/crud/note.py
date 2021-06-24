from typing import List
from app.schemas.note import NoteCreate, NoteUpdate
from sqlalchemy.orm import Session
from app.crud.models import Note
from app.context.context import AppContext
from fastapi.encoders import jsonable_encoder


class NoteDb:
    db: Session

    def __init__(self, context: AppContext):
        self.db = context.db

    def note_exists(self, folder_id: int, name: str) -> bool:
        query = self.db.query(Note) \
            .filter(Note.folder_id == folder_id) \
            .filter(Note.name == name)
        return self.db.query(query.exists()).scalar()

    def get_all(self, folder_id: int) -> List[Note]:
        return self.db.query(Note).filter(Note.folder_id == folder_id).all()

    def get(self, note_id: int) -> Note:
        return self.db.query(Note).filter(Note.id == note_id).one()

    def get_by_name(self, folder_id: int, name: str) -> Note:
        return self.db.query(Note) \
            .filter(Note.folder_id == folder_id) \
            .filter(Note.name == name) \
            .one()

    def create(self, folder_id: int, new_note: NoteCreate) -> Note:
        db_note = Note(
            folder_id=folder_id,
            name=new_note.name,
            shared=new_note.shared,
            type=new_note.type,
            text_body=new_note.text_body
        )
        self.db.add(db_note)
        self.db.commit()
        self.db.refresh(db_note)
        return db_note

    def update(self, note_id: int, note_update: NoteUpdate) -> Note:
        note = self.get(note_id)
        obj_data = jsonable_encoder(note)

        update_object = note_update.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_object:
                setattr(note, field, update_object[field])

        self.db.commit()
        return note

    def delete(self, note_id: int):
        note_db = self.get(note_id)
        self.db.delete(note_db)
        self.db.commit()
