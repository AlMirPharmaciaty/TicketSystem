from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from src.utils.database import Base
from sqlalchemy.sql import func


class TicketHistory(Base):
    __tablename__ = "ticketHistory"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    status = Column(String, nullable=False)