from app.api.workers.note_api import NoteApi
from app.crud.types import HeadingSort, SharedType
from app.schemas.note import NoteOut
from app.api.workers.folder_api import FolderApi
from typing import List, Optional
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
def get_all_auth(context: AppContextAuth = Depends(get_auth_context)):
    return FolderApi(context).get_all_default()


@router.get("/notes", response_model=List[NoteOut], description="Get all notes for user")
def get_all_notes(
    notes_per_page: int,
    page_nr: int,
    folder_id: Optional[int] = None,
    shared_filter: Optional[SharedType] = SharedType.NONE,
    node_text_filter: Optional[str] = None,
    shared_sorting: Optional[SharedType] = SharedType.NONE,
    heading_sorting: Optional[HeadingSort] = HeadingSort.NONE,
    context: AppContext = Depends(get_context)
):
    return NoteApi(context).get_all_default(folder_id, notes_per_page, page_nr, shared_filter, node_text_filter, shared_sorting, heading_sorting)


@router.get("/auth/notes", response_model=List[NoteOut], description="Get all notes for user. For authenticated users.")
def get_all_notes_auth(
    notes_per_page: int,
    page_nr: int,
    folder_id: Optional[int] = None,
    shared_filter: Optional[SharedType] = SharedType.NONE,
    node_text_filter: Optional[str] = None,
    shared_sorting: Optional[SharedType] = SharedType.NONE,
    heading_sorting: Optional[HeadingSort] = HeadingSort.NONE,
    context: AppContextAuth = Depends(get_auth_context)
):
    return NoteApi(context).get_all_default(folder_id, notes_per_page, page_nr, shared_filter, node_text_filter, shared_sorting, heading_sorting)
