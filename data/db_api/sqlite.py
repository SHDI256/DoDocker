from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data import config


def get_engine():
    engine = create_engine(f'sqlite:///{config.database_path}', echo=True)
    return engine


def get_session():
    engine = create_engine(f'sqlite:///{config.database_path}', echo=True)
    Session = sessionmaker(bind=engine)
    return Session()
