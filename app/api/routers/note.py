from typing import List
from app.api.workers.note_api import NoteApi
from app.schemas.note import NoteCreate, NoteOut, NoteUpdate
from app.context.auth_context import AppContextAuth, get_auth_context
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users/{user_id}/folders/{folder_id}/notes")


@router.post("", response_model=NoteOut, description="Create new note for user", status_code=201)
def create_note(folder_id: int, note: NoteCreate, context: AppContextAuth = Depends(get_auth_context)):
    return NoteApi(context).create(folder_id, note)


@router.put("/id", response_model=NoteOut, description="Update note with new name")
def update_note(note_id: int, note: NoteUpdate, context: AppContextAuth = Depends(get_auth_context)):
    return NoteApi(context).update(note_id, note)


@router.delete("/id", description="Delete note with id. Set force parameter to true if you want to recursively delete children notes.")
def delete_note(note_id: int, force: bool, context: AppContextAuth = Depends(get_auth_context)):
    return NoteApi(context).delete(note_id, force)


@router.get("", response_model=List[NoteOut], description="Get all notes for user")
def get_all(folder_id: int, context: AppContextAuth = Depends(get_auth_context)):
    return NoteApi(context).get_all(folder_id)


@router.get("/{id}", response_model=NoteOut)
def get(id: int, context: AppContextAuth = Depends(get_auth_context)):
    return NoteApi(context).get(id)


@router.get("/name/{name}", response_model=NoteOut)
def get_by_name(folder_id: int, name: str, context: AppContextAuth = Depends(get_auth_context)):
    return NoteApi(context).get_by_name(folder_id, name)
