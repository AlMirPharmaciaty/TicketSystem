from sqlalchemy import Column, DateTime, Integer, String, Boolean
from src.utils.database import Base
from sqlalchemy.sql import func

class TicketHistory(Base):
    __tablename__ = "ticketHistory"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)