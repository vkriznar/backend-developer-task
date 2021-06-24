from typing import List
from sqlalchemy.orm import Session
from app.crud.models import User
from app.schemas.user import UserCreate
from app.context.context import AppContext
from app.util.hash import get_password_hash


class UserDb:
    db: Session

    def __init__(self, context: AppContext):
        self.db = context.db

    def username_exists(self, user_name: str) -> bool:
        query = self.db.query(User) \
            .filter(User.username == user_name)
        return self.db.query(query.exists()).scalar()

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).one()

    def create(self, new_user: UserCreate) -> User:
        salt_hash = get_password_hash(new_user.password)
        db_user = User(
            name=new_user.name,
            username=new_user.username,
            hashed_password=salt_hash.hash,
            salt=salt_hash.salt
            )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
