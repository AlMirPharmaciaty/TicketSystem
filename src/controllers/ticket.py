from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.schemas.ticket import TicketCreate, TicketOrder
from src.models.ticket import Ticket, TicketHistory
from src.models.user import User
from src.schemas.ticket_status import TicketStatus


def get_my_tickets(
    db: Session,
    user: User,
    status: TicketStatus | None = None,
    skip: int = 0,
    limit: int = 10,
    order: TicketOrder = TicketOrder.LAT,
):
    tickets = db.query(Ticket).filter(Ticket.user_id == str(user.id))
    if status:
        tickets = tickets.filter(Ticket.status == status)
    if order.name == "OLD":
        tickets = tickets.order_by(Ticket.created_at.asc())
    else:
        tickets = tickets.order_by(Ticket.created_at.desc())

    return tickets.offset(skip).limit(limit).all()


def create_ticket(db: Session, ticket: TicketCreate, user: User):
    ticket = Ticket(
        **ticket.model_dump(),
        status=TicketStatus.NEW,
        user_id=user.id,
        username=user.username,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    history = TicketHistory(
        ticket_id=ticket.id,
        user_id=user.id,
        username=user.username,
        status=ticket.status,
    )
    db.add(history)
    db.commit()
    return ticket


def update_ticket_status(status: TicketStatus, ticket_id: int, db: Session, user: User):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=400, detail="Ticket not found.")

    ticket.status = status
    history = TicketHistory(
        ticket_id=ticket.id,
        user_id=user.id,
        username=user.username,
        status=status,
    )
    db.add(history)
    db.commit()
    return ticket


def get_ticket_history(ticket_id: int, db: Session):
    ticket = (
        db.query(TicketHistory)
        .filter(TicketHistory.ticket_id == ticket_id)
        .order_by(TicketHistory.created_at.desc())
        .all()
    )
    return ticket
