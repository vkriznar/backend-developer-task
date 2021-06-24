from typing import List
from app.schemas.folder import FolderCreate
from sqlalchemy.orm import Session
from app.crud.models import Folder
from app.context.context import AppContext


class FolderDb:
    db: Session

    def __init__(self, context: AppContext):
        self.db = context.db

    def folder_exists(self, user_id: int, name: str) -> bool:
        query = self.db.query(Folder) \
            .filter(Folder.user_id == user_id) \
            .filter(Folder.name == name)
        return self.db.query(query.exists()).scalar()

    def get_all(self, user_id: int) -> List[Folder]:
        return self.db.query(Folder).filter(Folder.user_id == user_id).all()

    def get(self, folder_id: int) -> Folder:
        return self.db.query(Folder).filter(Folder.id == folder_id).one()

    def get_by_name(self, user_id: int, name: str) -> Folder:
        return self.db.query(Folder) \
            .filter(Folder.user_id == user_id) \
            .filter(Folder.name == name) \
            .one()

    def create(self, user_id: int, new_folder: FolderCreate) -> Folder:
        db_folder = Folder(
            user_id=user_id,
            name=new_folder.name
        )
        self.db.add(db_folder)
        self.db.commit()
        self.db.refresh(db_folder)
        return db_folder
