from app.api.workers.folder_api import FolderApi
from typing import List
from app.schemas.folder import FolderOut
from app.context.context import AppContext, get_context
from app.context.auth_context import AppContextAuth, get_auth_context
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/default")


# Following routes do not require users to be authenticated however only open data will be shown
@router.get("/folders", response_model=List[FolderOut], description="Get all folders for user")
def get_all(context: AppContext = Depends(get_context)):
    return FolderApi(context).get_all_default()


@router.get("/auth/folders", response_model=List[FolderOut], description="Get all folders for user. For authenticated users.")
def get_all_authenticated(context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).get_all_default()
