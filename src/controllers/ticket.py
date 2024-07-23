from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.ticket import TicketCreate
from src.models.ticket import Ticket
from src.models.user import User
from src.schemas.ticket_status import TicketStatus


def create_ticket(db: Session, ticket: TicketCreate, user: User):
    ticket = Ticket(
        **ticket.model_dump(),
        status=TicketStatus.NEW,
        user_id=user.id,
        username=user.username,
    )
    db.add(ticket)
    db.commit()
    return ticket


def get_user_tickets(db: Session, user: User):
    query = db.query(Ticket).filter(Ticket.user_id == user.user_id).all()
    return query