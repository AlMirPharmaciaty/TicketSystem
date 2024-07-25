from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.utils.database import get_db
from src.utils.auth import RoleChecker
from src.models.user import User
from src.schemas.api_response import APIResponse
from src.schemas.ticket import TicketNoteCreate
from src.controllers.ticket import TicketController
from src.controllers.ticket_notes import TicketNotesController

ticket_notes = APIRouter(prefix="/notes", tags=["Ticket Notes"])


@ticket_notes.get("/", response_model=APIResponse)
def note_get(
    ticket_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer", "Pharmacist"])),
):
    response = APIResponse()

    try:
        ticket_controller = TicketController(db=db)
        user_id = None if "Pharmacist" in user.roles else user.id
        ticket = ticket_controller.get_tickets(ticket_id=ticket_id, user_id=user_id)
        if not ticket:
            raise Exception("Ticket not found.")

        note_controller = TicketNotesController(db=db)
        response.data = jsonable_encoder(note_controller.get_notes(ticket_id=ticket_id))
        response.status = "success"
    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@ticket_notes.post("/", response_model=APIResponse)
def note_create(
    note: TicketNoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer", "Pharmacist"])),
):
    response = APIResponse()

    try:
        ticket_controller = TicketController(db=db)
        user_id = None if "Pharmacist" in user.roles else user.id
        ticket = ticket_controller.get_tickets(
            ticket_id=note.ticket_id, user_id=user_id
        )
        if not ticket:
            raise Exception("Ticket not found.")

        note_controller = TicketNotesController(db=db)
        data = note_controller.create_note(note=note, user=user)
        response.data = jsonable_encoder([data])
        response.status = "success"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response
