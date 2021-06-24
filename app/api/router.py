from fastapi import APIRouter
from app.api.routers import auth, default, folder, note, user, list


api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(default.router, tags=["default"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(folder.router, tags=["folder"])
api_router.include_router(note.router, tags=["note"])
api_router.include_router(list.router, tags=["list"])
