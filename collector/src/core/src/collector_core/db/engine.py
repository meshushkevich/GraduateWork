from sqlalchemy import create_engine

_engine = create_engine("sqlite:///collector.db", echo=False)


def get_engine():
    return _engine
