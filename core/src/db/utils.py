from sqlalchemy.orm import sessionmaker
from src.db.engine import get_engine
from src.db.models import Base

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
