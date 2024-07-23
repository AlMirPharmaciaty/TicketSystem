from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controllers.ticket import create_ticket
from src.schemas.ticket import TicketCreate, TicketDetails
from src.models.user import User
from src.utils.database import get_db
from src.utils.auth import RoleChecker

tickets = APIRouter(prefix="/tickets", tags=["Tickets"])


@tickets.post("/", response_model=TicketDetails)
async def ticket_create(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    return create_ticket(ticket=ticket, user=user, db=db)
