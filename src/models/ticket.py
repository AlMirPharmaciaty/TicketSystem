from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from src.utils.database import Base


class BaseTicket(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    status = Column(String, nullable=False, default="New")


class Ticket(BaseTicket):
    __tablename__ = "tickets"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)


class TicketHistory(BaseTicket):
    __tablename__ = "ticketHistory"

    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)


class TicketNote(BaseTicket):
    __tablename__ = "ticketNotes"

    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    note = Column(Text, nullable=False)
