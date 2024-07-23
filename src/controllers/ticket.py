from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import ticket as ticket_schema
from src.models import ticket as ticket_model 
from src.models import user as user_model
from src.schemas.ticketStatus import TicketStatus
from datetime import datetime

def create_ticket(db: Session, ticket: ticket_schema.TicketCreate, user: user_model.User):
    new_ticket = ticket_model.Ticket(
        title = ticket.title,
        description = ticket.description,
        status = "New",
        user_id = user.id,
        username = user.username
    )

    db.add(new_ticket)
    db.commit()
    return new_ticket

<<<<<<< Updated upstream
def get_tickets_user(db: Session, user: user_model.User):
    query = db.query(ticket_model.Ticket).filter(ticket_model.Ticket.username == user.username).all()
    if query == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Tickets Raised")
    return query
=======

def get_user_tickets(db: Session, user: User):
    query = db.query(Ticket).filter(Ticket.user_id == str(user.user_id)).all()
    return query

def get_tickets(db: Session, user: User, user_id: str | None = None, status: TicketStatus | None = None):
    query = db.query(Ticket)
    if user_id:
        query = query.filter(Ticket.user_id == user_id)
    if status:
        query = query.filter(Ticket.status == status)
    return query.all()
>>>>>>> Stashed changes
