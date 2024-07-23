from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
<<<<<<< Updated upstream
from src.controllers.ticket import create_ticket, get_tickets_user
from src.schemas import ticket as ticket_schema
from src.models import ticket as ticket_models
from src.models import user as user_models
=======
from src.controllers.ticket import create_ticket, get_tickets, get_user_tickets
from src.schemas.ticket import TicketCreate, TicketDetails
from src.models.user import User
from src.schemas.ticket_status import TicketStatus
>>>>>>> Stashed changes
from src.utils.database import get_db
from src.utils.auth import RoleChecker
tickets = APIRouter(prefix="/tickets", tags=["Tickets"])

@tickets.post("/create", response_model= ticket_schema.TicketDetails)
async def createTicket(ticket: ticket_schema.TicketCreate, user: user_models.User= Depends(RoleChecker(allowed_roles=["Customer"])),db: Session = Depends(get_db)):
    return create_ticket(ticket=ticket, user=user, db=db)

<<<<<<< Updated upstream
@tickets.get("/user", response_model=list[ticket_schema.TicketDetails])
async def getTicketsUser(user: user_models.User = Depends(RoleChecker(allowed_roles=["Customer"])), db: Session = Depends(get_db)):
    return get_tickets_user(user=user, db=db)
=======

@tickets.get("/", response_model=list[TicketDetails])
async def ticket_get_user(
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
    db: Session = Depends(get_db),
):
    return get_user_tickets(user=user, db=db)

@tickets.get("/all", response_model=list[TicketDetails])
async def ticket_get_all(
    user_id: str | None = None,
    status: TicketStatus | None = None,
    user: User = Depends(RoleChecker(allowed_roles=["Pharmacist"])),
    db: Session = Depends(get_db)
):
    return get_tickets(db=db, user=user, user_id=user_id, status=status)
>>>>>>> Stashed changes
