from datetime import datetime
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import status
from sqlalchemy.orm.session import Session
from app.context.auth import Auth, TokenData
from app.context.context import AppContext, get_context
from app.schemas.user import UserOut


class AppContextAuth(AppContext):
    user: UserOut

    def __init__(self, db: Session, user: UserOut, base_context: AppContext):
        super().__init__(db, base_context.settings)
        self.user = user

    def dispose(self):
        super().dispose()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")


def get_auth_context(context: AppContext = Depends(get_context), token: str = Depends(oauth2_scheme)):
    """Parses current user from provided json token string and return authenticated context"""
    auth = Auth(context)
    try:
        signing_key = auth.get_key()
        payload: dict = auth.jwt.decode(token, signing_key, do_time_check=False)

        token_id: Optional[str] = payload.get("token_id")
        sub: Optional[str] = payload.get("sub")
        exp: Optional[int] = payload.get("exp")

        if token_id is None or sub is None or (exp is not None and datetime.fromtimestamp(exp) < datetime.now()):
            raise auth.CREDENTIALS_EXCEPTION
        token_data = TokenData(token_id, sub, exp)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token, expired or revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth.user_api.get_by_username(token_data.sub)
    auth_context = AppContextAuth(context.db, user, context)

    try:
        yield auth_context
    finally:
        auth_context.dispose()
