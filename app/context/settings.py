from functools import lru_cache
from pydantic import BaseSettings
from os import getenv


class AppSettings(BaseSettings):
    db_url: str
    admin_user: str = "admin"

    hs_key: str

    class Config:
        env_prefix = 'CELTRA_'
        env_file = 'app.env'
        env_file_encoding = 'utf-8'


@lru_cache(maxsize=3)
def get_app_settings() -> AppSettings:
    config_env = "CELTRA_config_file"
    config_file = getenv(config_env, "app.env")
    return AppSettings(_env_file=config_file)


# clear cache on app reload
get_app_settings.cache_clear()
