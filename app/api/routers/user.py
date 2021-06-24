from app.context.auth_context import AppContextAuth, get_auth_context
from app.context.context import AppContext, get_context
from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserOut
from app.api.workers.user_api import UserApi

router = APIRouter(prefix="/users")


@router.post("", response_model=UserOut)
def create_user(user: UserCreate, context: AppContextAuth = Depends(get_auth_context)):
    return UserApi(context).create_user(user)
