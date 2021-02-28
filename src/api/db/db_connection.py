import sqlalchemy
from api import app_configs
from functools import lru_cache


@lru_cache
def init_engine():
    db_url = app_configs.DB_URL
    engine = sqlalchemy.create_engine(db_url)
    return engine
