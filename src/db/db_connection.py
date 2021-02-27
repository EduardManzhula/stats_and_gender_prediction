import configparser
import sqlalchemy
from functools import lru_cache


@lru_cache
def init_engine():
    config = configparser.ConfigParser()
    config.read("configs/credentials.ini")
    eng = config['connection']['engine']
    hst = config['connection']['hostname']
    prt = config['connection']['port']
    usr = config['connection']['username']
    pwd = config['connection']['password']
    scm = config['connection']['schema']
    db_url = f'{eng}://{usr}:{pwd}@{hst}:{prt}/{scm}'
    engine = sqlalchemy.create_engine(db_url)
    return engine
