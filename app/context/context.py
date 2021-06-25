from contextlib import contextmanager
from typing import Callable, Optional
from app.context.settings import AppSettings, get_app_settings
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session, sessionmaker


class AppContext:
    db: Session
    settings: AppSettings

    def __init__(self, db: Session, settings: AppSettings = Depends(get_app_settings)) -> None:
        self.db = db
        self.settings = settings

    def dispose(self):
        if self.db is not None:
            self.db.close()


def get_context(settings: AppSettings = Depends(get_app_settings)):
    SessionLocal = get_session_factory(settings)
    database: Session = SessionLocal()
    context = AppContext(database, settings)
    try:
        yield context
    finally:
        context.dispose()


@contextmanager
def get_plain_context(settings_provider: Optional[Callable[[], AppSettings]]):
    settings_callable = settings_provider or get_app_settings
    settings = settings_callable()
    SessionLocal = get_session_factory(settings)
    database: Session = SessionLocal()
    context = AppContext(database, settings)
    try:
        yield context
    finally:
        context.dispose()


def get_engine(db_url: str):
    connect_args = {}
    if db_url.startswith("sqlite:"):
        connect_args = {"check_same_thread": False}
        return create_engine(db_url, connect_args=connect_args)

    return create_engine(db_url)


def get_session_factory(settings: AppSettings) -> sessionmaker:
    engine = get_engine(settings.db_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
