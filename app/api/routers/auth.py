from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.context.auth import Auth, Token
from app.context.context import AppContext, get_context


router = APIRouter(prefix="/token")


@router.post("", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), context: AppContext = Depends(get_context)):
    auth = Auth(context)
    user = auth.authenticate_user(form_data.username, form_data.password)  # type: ignore
    if not user:
        raise auth.CREDENTIALS_EXCEPTION
    access_token = auth.create_web_access_token(user.username)
    return Token(access_token=access_token, token_type="bearer")
