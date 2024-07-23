from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.ticket import Ticket
from src.models.ticket_notes import TicketNote
from src.models.user import User
from src.schemas.ticket_notes import TicketNoteCreate


def create_note(note: TicketNoteCreate, db: Session, user: User):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == note.ticket_id,
            Ticket.status not in ["Completed", "Cancelled", "Rejected"],
        )
        .first()
    )
    if not ticket:
        raise HTTPException(status_code=400, detail="Ticket not found.")
    note = TicketNote(**note.model_dump(), user_id=user.id, username=user.username)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
