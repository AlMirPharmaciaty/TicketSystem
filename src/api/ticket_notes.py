from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.controllers.ticket_notes import get_notes, create_note
from src.schemas.ticket_notes import TicketNoteDetails, TicketNoteCreate
from src.models.user import User
from src.utils.auth import RoleChecker

ticket_notes = APIRouter(prefix="/notes", tags=["Ticket Notes"])


@ticket_notes.get("/", response_model=list[TicketNoteDetails])
def note_get(
    ticket_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer", "Pharmacist"])),
):
    if "Customer" in user.roles:
        return get_notes(ticket_id=ticket_id, db=db, user=user)
    else:
        return get_notes(ticket_id=ticket_id, db=db)


@ticket_notes.post("/", response_model=TicketNoteDetails)
def note_create(
    note: TicketNoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    return create_note(note=note, db=db, user=user)
