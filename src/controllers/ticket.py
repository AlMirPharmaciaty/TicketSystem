from sqlalchemy.orm import Session

from src.schemas.ticket import TicketCreate, TicketStatus, TicketOrder
from src.models.ticket import Ticket, TicketHistory
from src.models.user import User


class TicketController:
    def __init__(self, db: Session):
        self.db = db

    def update_ticket_history(self, ticket: Ticket, user: User):
        self.db.flush()
        history = TicketHistory(
            ticket_id=ticket.id,
            status=ticket.status,
            user_id=user.id,
            username=user.username,
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(ticket)

    def get_tickets(
        self,
        user_id: str | None = None,
        ticket_id: int | None = None,
        status: TicketStatus | None = None,
        skip: int = 0,
        limit: int = 10,
        order: TicketOrder = TicketOrder.NEW,
    ):
        tickets = self.db.query(Ticket)
        if user_id:
            tickets = tickets.filter(Ticket.user_id == str(user_id))
        if ticket_id:
            tickets = tickets.filter(Ticket.id == ticket_id)
        if status:
            tickets = tickets.filter(Ticket.status == status)
        tickets = tickets.order_by(
            Ticket.created_at.asc() if order.name == "OLD" else Ticket.created_at.desc()
        )
        return tickets.offset(skip).limit(limit).all()

    def create_ticket(self, ticket: TicketCreate, user: User):
        ticket = Ticket(
            **ticket.model_dump(),
            status=TicketStatus.NEW,
            user_id=user.id,
            username=user.username,
        )
        self.db.add(ticket)
        self.update_ticket_history(ticket=ticket, user=user)
        return ticket

    def update_ticket_status(self, status: TicketStatus, ticket: Ticket, user: User):
        ticket.status = status
        self.update_ticket_history(ticket=ticket, user=user)
        return ticket

    def get_ticket_history(self, ticket: Ticket):
        history = (
            self.db.query(TicketHistory)
            .filter(TicketHistory.ticket_id == ticket.id)
            .order_by(TicketHistory.created_at.desc())
            .all()
        )
        return history
