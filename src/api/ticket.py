from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.utils.database import get_db
from src.utils.auth import RoleChecker
from src.models.ticket import Ticket
from src.models.user import User
from src.schemas.api_response import APIResponse
from src.schemas.ticket import TicketCreate, TicketStatus, TicketOrder
from src.controllers.ticket import TicketController

tickets = APIRouter(prefix="/tickets", tags=["Tickets"])


@tickets.get("/", response_model=APIResponse)
async def ticket_get(
    ticket_id: int | None = None,
    user_id: str | None = None,
    status: TicketStatus | None = None,
    skip: int = 0,
    limit: int = 10,
    order: TicketOrder = TicketOrder.NEW,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer", "Pharmacist"])),
):
    response = APIResponse()

    try:
        if (user_id and "Pharmacist" in user.roles) or "Pharmacist" in user.roles:
            user_id = user_id
        else:
            user_id = str(user.id)

        controller = TicketController(db=db)
        data = controller.get_tickets(
            user_id=user_id,
            ticket_id=ticket_id,
            status=status,
            skip=skip,
            limit=limit,
            order=order,
        )
        response.data = jsonable_encoder(data)
        response.status = "success"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@tickets.post("/", response_model=APIResponse)
async def ticket_create(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    response = APIResponse()

    try:
        controller = TicketController(db=db)
        data = controller.create_ticket(ticket=ticket, user=user)
        response.data = jsonable_encoder([data])
        response.status = "success"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@tickets.put("/", response_model=APIResponse)
async def ticket_status_update(
    ticket_id: int,
    status: TicketStatus,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Pharmacist"])),
):
    response = APIResponse()

    try:
        controller = TicketController(db=db)
        ticket = controller.get_tickets(ticket_id=ticket_id)
        if not ticket:
            raise Exception("Ticket not found.")
        ticket = ticket[0]
        data = controller.update_ticket_status(status=status, ticket=ticket, user=user)
        response.data = jsonable_encoder([data])
        response.status = "success"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@tickets.get("/history/", response_model=APIResponse)
async def ticket_history(
    ticket_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer", "Pharmacist"])),
):
    response = APIResponse()

    try:
        controller = TicketController(db=db)
        user_id = None if "Pharmacist" not in user.roles else str(user.id)
        ticket = controller.get_tickets(ticket_id=ticket_id, user_id=user_id)
        if not ticket:
            raise Exception("Ticket not found.")
        ticket = ticket[0]
        response.data = jsonable_encoder(controller.get_ticket_history(ticket=ticket))
        response.status = "success"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response
