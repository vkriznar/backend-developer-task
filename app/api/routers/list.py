# from typing import List
from app.api.workers.list_api import ListApi
from app.schemas.list import ListCreate, ListOut, ListUpdate
from app.context.auth_context import AppContextAuth, get_auth_context
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users/{user_id}/folders/{folder_id}/notes/{note_id}/lists")


@router.post("", response_model=ListOut, description="Create new list for note", status_code=201)
def create_list(note_id: int, list: ListCreate, context: AppContextAuth = Depends(get_auth_context)):
    return ListApi(context).create(note_id, list)


@router.put("/id", response_model=ListOut, description="Update list with new name")
def update_list(list_id: int, list: ListUpdate, context: AppContextAuth = Depends(get_auth_context)):
    return ListApi(context).update(list_id, list)


@router.delete("/id", description="Delete list with id.")
def delete_list(list_id: int, context: AppContextAuth = Depends(get_auth_context)):
    return ListApi(context).delete(list_id)


""" @router.get("", response_model=List[ListOut], description="Get all lists for note")
def get_all(note_id: int, context: AppContextAuth = Depends(get_auth_context)):
    return ListApi(context).get_all(note_id)


@router.get("/{id}", response_model=ListOut)
def get(id: int, context: AppContextAuth = Depends(get_auth_context)):
    return ListApi(context).get(id) """
