from fastapi import APIRouter
from app.api.routers import auth, folder, note, user


api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(folder.router, tags=["folder"])
api_router.include_router(note.router, tags=["note"])
