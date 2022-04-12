from data import config


if config.database == "sqlite":
    from .sqlite import get_engine, get_session
else:
    from .postgrest import get_session

#Session = get_session()