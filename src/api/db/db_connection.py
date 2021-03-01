from functools import lru_cache

import sqlalchemy

from api import app_configs


@lru_cache
def init_engine():
    db_url = app_configs.DB_URL
    engine = sqlalchemy.create_engine(db_url)
    return engine
