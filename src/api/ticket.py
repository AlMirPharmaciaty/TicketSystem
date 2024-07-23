from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from src.controllers.ticket import create_ticket, get_tickets_user
from src.schemas import ticket as ticket_schema
from src.models import ticket as ticket_models
from src.models import user as user_models
from src.utils.database import get_db
from src.utils.auth import RoleChecker
tickets = APIRouter(prefix="/tickets", tags=["Tickets"])

@tickets.post("/create", response_model= ticket_schema.TicketDetails)
async def createTicket(ticket: ticket_schema.TicketCreate, user: user_models.User= Depends(RoleChecker(allowed_roles=["Customer"])),db: Session = Depends(get_db)):
    return create_ticket(ticket=ticket, user=user, db=db)

@tickets.get("/user", response_model=list[ticket_schema.TicketDetails])
async def getTicketsUser(user: user_models.User = Depends(RoleChecker(allowed_roles=["Customer"])), db: Session = Depends(get_db)):
    return get_tickets_user(user=user, db=db)
