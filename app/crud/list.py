from app.crud.models import ListDbModel
from typing import List
from app.schemas.list import ListCreate, ListUpdate
from sqlalchemy.orm import Session
from app.context.context import AppContext
from fastapi.encoders import jsonable_encoder


class ListDb:
    db: Session

    def __init__(self, context: AppContext):
        self.db = context.db

    def list_exists(self, note_id: int, text_body: str) -> bool:
        query = self.db.query(ListDbModel) \
            .filter(ListDbModel.note_id == note_id) \
            .filter(ListDbModel.text_body == text_body)
        return self.db.query(query.exists()).scalar()

    def get_all(self, note_id: int) -> List[ListDbModel]:
        return self.db.query(ListDbModel).filter(ListDbModel.note_id == note_id).all()

    def get(self, list_id: int) -> ListDbModel:
        return self.db.query(ListDbModel).filter(ListDbModel.id == list_id).one()

    def create(self, note_id: int, new_list: ListCreate) -> ListDbModel:
        db_list = ListDbModel(
            note_id=note_id,
            text_body=new_list.text_body
        )
        self.db.add(db_list)
        self.db.commit()
        self.db.refresh(db_list)
        return db_list

    def update(self, list_id: int, list_update: ListUpdate) -> ListDbModel:
        list = self.get(list_id)
        obj_data = jsonable_encoder(list)

        update_object = list_update.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_object:
                setattr(list, field, update_object[field])

        self.db.commit()
        return list

    def delete(self, list_id: int):
        list_db = self.get(list_id)
        self.db.delete(list_db)
        self.db.commit()
