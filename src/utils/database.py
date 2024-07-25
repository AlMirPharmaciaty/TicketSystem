from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.settings import Settings

settings = Settings()
engine = create_engine(settings.get_db_url())
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
