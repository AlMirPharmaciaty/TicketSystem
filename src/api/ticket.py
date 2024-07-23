from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.ticket import (
    create_ticket,
    get_my_tickets,
    update_ticket_status,
    get_ticket_history,
)
from src.schemas.ticket import TicketCreate, TicketDetails, TicketOrder
from src.schemas.ticket_history import TicketHistoryDetails

from src.models.user import User
from src.utils.database import get_db
from src.utils.auth import RoleChecker
from src.schemas.ticket_status import TicketStatus

tickets = APIRouter(prefix="/tickets", tags=["Tickets"])


@tickets.get("/", response_model=list[TicketDetails])
async def ticket_get_my(
    status: TicketStatus | None = None,
    skip: int = 0,
    limit: int = 10,
    order: TicketOrder = TicketOrder.LAT,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    return get_my_tickets(
        db=db,
        user=user,
        status=status,
        skip=skip,
        limit=limit,
        order=order,
    )


@tickets.get("/all/", response_model=list[TicketDetails])
async def ticket_get_all(
    user_id: str | None = None,
    status: TicketStatus | None = None,
    skip: int = 0,
    limit: int = 10,
    order: TicketOrder = TicketOrder.LAT,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Pharmacist"])),
):
    return get_my_tickets(
        db=db,
        user=user,
        user=user_id,
        status=status,
        skip=skip,
        limit=limit,
        order=order,
    )


@tickets.post("/", response_model=TicketDetails)
async def ticket_create(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    return create_ticket(ticket=ticket, user=user, db=db)


@tickets.put("/", response_model=TicketDetails)
async def ticket_status_update(
    ticket_id: int,
    status: TicketStatus,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Pharmacist"])),
):
    return update_ticket_status(status=status, ticket_id=ticket_id, db=db, user=user)


@tickets.get("/history/", response_model=list[TicketHistoryDetails])
async def ticket_history(ticket_id: int, db: Session = Depends(get_db)):
    return get_ticket_history(ticket_id=ticket_id, db=db)
