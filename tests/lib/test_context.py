import os
from tests.database.db_helper import DbHelper
from fastapi import FastAPI
from alembic import config, command
from app.context.context import get_plain_context
from app.context.settings import AppSettings
from app.api.router import api_router


def create_test_client():
    app = FastAPI(title="TEST Celtra app")
    app.include_router(api_router)

    alembic_cfg = config.Config(
        config_args={
            "db_url": get_test_settings().db_url,
        },
        file_="alembic/alembic.ini"
    )
    alembic_cfg.set_main_option('script_location', "alembic")
    command.upgrade(alembic_cfg, 'head')

    with get_plain_context(get_test_settings) as context:
        db_helper = DbHelper(context)
        db_helper.mock_db_data()

    from fastapi.testclient import TestClient
    return TestClient(app)


def cleanup_db():
    if os.path.exists("test-db.temp"):
        os.remove("test-db.temp")


def get_test_settings() -> AppSettings:
    return AppSettings(
        db_url="sqlite:///test-db.temp",
        hs_key="m11sWkG7AAMhxgZUbk8Y1CBW/qq2TVJBcZK+XjLF60AsUu7blKpixdFsRtm60VGotCgxSI1IlTSOyFnql1bl4w=="
    )
