from fastapi import FastAPI
from app.api.router import api_router


app = FastAPI(
    title="Celtra API",
    description="Simple fastapi api used for managing notes.")


app.include_router(api_router, prefix="/api/v1")
