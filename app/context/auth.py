from datetime import datetime, timedelta
from typing import NamedTuple, Optional
from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from pydantic.main import BaseModel
from app.api.workers.user_api import UserApi
from app.context.context import AppContext, get_context
from app.crud.user import UserDb
from app.crud.models import User
from app.schemas.user import UserOut
from app.util.hash import is_valid_password
from jwt.jwt import JWT
from jwt.jwk import jwk_from_dict
import uuid


class Token(BaseModel):
    """Access token with data and token type [bearer]"""
    access_token: str
    token_type: str


class TokenData(NamedTuple):
    """Holds data for Acess Token"""
    token_id: str
    sub: str
    exp: Optional[int]


class Auth():
    """Authentication class using fastapi and jwt"""
    context: AppContext
    user_api: UserApi
    jwt: JWT

    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def __init__(self, context: AppContext = Depends(get_context)):
        self.context = context
        self.user_api = UserApi(context)
        self.user_db = UserDb(context)

        self.jwt = JWT()

    def authenticate_user(self, username: str, password: str) -> UserOut:
        """Authenticate user with username and password"""
        if not self.user_db.username_exists(username):
            self.raise_auth_exception()

        user: User = self.user_db.get_by_username(username)

        if not is_valid_password(user.salt, user.hashed_password, password):
            self.raise_auth_exception()
        return user

    def raise_auth_exception(self):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect username and password")

    def create_web_access_token(self, username: str, exp_minutes: int = 30) -> str:
        """Create access token for user"""
        now = datetime.now()
        expire = now + timedelta(minutes=exp_minutes)
        token_id = str(uuid.uuid4())
        return self.create_jwt(token_id, username, expire)

    def create_jwt(self, token_id: str, username: str, valid_until: datetime) -> str:
        epoch_expiry = int(valid_until.timestamp())
        payload = {
            "token_id": token_id,
            "sub": username,
            "exp": epoch_expiry
        }
        key = self.get_key()
        return self.jwt.encode(payload, key, alg='HS256')

    def get_key(self):
        key = {
            "kty": "oct",
            "k": self.context.settings.hs_key
        }
        return jwk_from_dict(key)
