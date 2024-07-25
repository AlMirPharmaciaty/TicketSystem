from sqlalchemy.orm import Session

from src.models.ticket import TicketNote
from src.models.user import User
from src.schemas.ticket import TicketNoteCreate


class TicketNotesController:
    def __init__(self, db: Session):
        self.db = db

    def get_notes(self, ticket_id: int):
        notes = (
            self.db.query(TicketNote)
            .filter(TicketNote.ticket_id == ticket_id)
            .order_by(TicketNote.created_at.desc())
            .all()
        )
        return notes

    def create_note(self, note: TicketNoteCreate, user: User):
        note = TicketNote(
            **note.model_dump(),
            user_id=user.id,
            username=user.username,
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
