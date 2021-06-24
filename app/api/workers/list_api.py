from typing import List
from app.crud.list import ListDb
from app.schemas.list import ListCreate, ListOut, ListUpdate
from sqlalchemy.orm import Session
from app.context.context import AppContext


class ListApi:
    db: Session

    def __init__(self, context: AppContext):
        self.db = context.db
        self.list_db = ListDb(context)

    def create(self, note_id: int, list: ListCreate) -> ListOut:
        return self.list_db.create(note_id, list)

    def update(self, list_id: int, list_update: ListUpdate) -> ListOut:
        return self.list_db.update(list_id, list_update)

    def delete(self, list_id: int):
        self.list_db.delete(list_id)

    def get_all(self, note_id: int) -> List[ListOut]:
        return self.list_db.get_all(note_id)

    def get(self, list_id: int) -> ListOut:
        return self.list_db.get(list_id)
