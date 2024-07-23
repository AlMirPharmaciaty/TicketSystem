from datetime import datetime
from pydantic import BaseModel


class TicketNoteBase(BaseModel):
    ticket_id: int
    note: str


class TicketNoteDetails(TicketNoteBase):
    id: int
    created_at: datetime
    user_id: str
    username: str


class TicketNoteCreate(TicketNoteBase):
    pass
