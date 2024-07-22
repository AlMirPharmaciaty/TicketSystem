from sqlalchemy import Column, Integer, String, Boolean, DateTime, ARRAY
from sqlalchemy.sql import func
from ..utils.database import Base

func: callable


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)
    roles = Column(ARRAY(String))