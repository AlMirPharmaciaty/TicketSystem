from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.utils.database import Base

func: callable


class TicketNote(Base):
    __tablename__ = "ticketNotes"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    note = Column(Text, nullable=False)