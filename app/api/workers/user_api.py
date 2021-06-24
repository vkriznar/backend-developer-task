from sqlalchemy.orm import Session
from app.context.context import AppContext
from app.crud.user import UserDb
from app.schemas.user import UserCreate, UserOut
from fastapi import HTTPException, status


class UserApi:
    db: Session

    def __init__(self, context: AppContext):
        self.db = context.db
        self.user_db = UserDb(context)

    def __check_username_exist__(self, username: str):
        if not self.user_db.username_exists(username):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"User with '{username}' doesn't exist")

    def __check_username_not_exist__(self, username: str):
        if self.user_db.username_exists(username):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"User with '{username}' already exists")

    def create_user(self, user: UserCreate) -> UserOut:
        self.__check_username_not_exist__(user.username)
        return self.user_db.create(user)

    def get_by_username(self, username: str) -> UserOut:
        self.__check_username_exist__(username)
        return self.user_db.get_by_username(username)
