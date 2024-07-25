from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.utils.database import get_db
from src.utils.auth import RoleChecker
from src.models.ticket import Ticket
from src.models.user import User
from src.schemas.api_response import APIResponse
from src.schemas.ticket import TicketNoteCreate
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
        # Get ticket by Id
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id)
        # Check if user is not a Pharmacist
        if "Pharmacist" not in user.roles:
            # Restrict to tickets created by the user
            ticket = ticket.filter(Ticket.user_id == str(user.id))
        ticket = ticket.first()

        # Raise an exception if ticket not found
        if not ticket:
            raise Exception("Ticket not found.")

        # Pass the ticket id to the controller
        # to get list of notes based on ticket id
        controller = TicketNotesController(db=db)
        response.data = jsonable_encoder(controller.get_notes(ticket_id=ticket_id))
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
        # Get ticket by Id
        ticket = db.query(Ticket).filter(Ticket.id == note.ticket_id)
        # check if ticket is still open
        ticket = ticket.filter(
            Ticket.status not in ["Completed", "Cancelled", "Rejected"]
        )
        # Check if user is not a Pharmacist
        if "Pharmacist" not in user.roles:
            # Restrict to tickets created by the user
            ticket = ticket.filter(Ticket.user_id == str(user.id))
        ticket = ticket.first()
        # Raise and exception if ticket not found
        if not ticket:
            raise Exception("Ticket not found.")

        # Pass the data to the controller
        # to add a new note to the ticket
        controller = TicketNotesController(db=db)
        data = controller.create_note(note=note, user=user)
        response.data = jsonable_encoder([data])

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response
