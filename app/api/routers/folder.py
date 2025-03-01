from typing import List, Optional
from app.api.workers.folder_api import FolderApi
from app.schemas.folder import FolderCreate, FolderOut, FolderUpdate
from app.context.auth_context import AppContextAuth, get_auth_context
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users/{user_id}/folders")


@router.post("", response_model=FolderOut, description="Create new folder for user", status_code=201)
def create_folder(user_id: int, folder: FolderCreate, context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).create(user_id, folder)


@router.put("/{id}", response_model=FolderOut, description="Update folder with new name", status_code=200)
def update_folder(user_id: int, id: int, folder: FolderUpdate, context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).update(user_id, id, folder)


@router.delete("/{id}", description="Delete folder with id. Set force parameter to true if you want to recursively delete children notes.")
def delete_folder(user_id: int, id: int, force: bool, context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).delete(user_id, id, force)


@router.get("", response_model=List[FolderOut], description="Get all folders for user")
def get_all(user_id: Optional[int], context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).get_all(user_id)


@router.get("/{id}", response_model=FolderOut)
def get(user_id: int, id: int, context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).get(id)


@router.get("/name/{name}", response_model=FolderOut)
def get_by_name(user_id: str, name: str, context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).get_by_name(user_id, name)
