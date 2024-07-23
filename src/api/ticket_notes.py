from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.controllers.ticket_notes import create_note
from src.schemas.ticket_notes import TicketNoteDetails, TicketNoteCreate
from src.models.user import User
from src.utils.auth import RoleChecker

ticket_notes = APIRouter(prefix="/notes", tags=["Ticket Notes"])


@ticket_notes.post("/", response_model=TicketNoteDetails)
def note_create(
    note: TicketNoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(RoleChecker(allowed_roles=["Customer"])),
):
    return create_note(note=note, db=db, author_id=user.id)
