from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controllers.ticket import create_ticket, get_user_tickets, get_all_tickets
from src.schemas.ticket import TicketCreate, TicketDetails, TicketOrder
from src.models.user import User
from src.utils.database import get_db
from src.utils.auth import RoleChecker
from src.schemas.ticket_status import TicketStatus

tickets = APIRouter(prefix="/tickets", tags=["Tickets"])


@tickets.post("/", response_model=TicketDetails)
async def ticket_create(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    return create_ticket(ticket=ticket, user=user, db=db)


@tickets.get("/", response_model=list[TicketDetails])
async def ticket_get_my(
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
    skip: int = 0,
    limit: int = 10,
    order: TicketOrder = TicketOrder.LAT,
):
    return get_user_tickets(db=db, user=user)


@tickets.get("/all", response_model=list[TicketDetails])
async def ticket_get_all(
    user_id: str | None = None,
    status: TicketStatus | None = None,
    skip: int = 0,
    limit: int = 10,
    order: TicketOrder = TicketOrder.LAT,
    db: Session = Depends(get_db),
    _: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    return get_all_tickets(
        db=db, user_id=user_id, status=status, skip=skip, limit=limit, order=order
    )
