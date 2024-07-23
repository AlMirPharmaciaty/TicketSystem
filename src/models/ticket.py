from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from src.utils.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default="New")
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)