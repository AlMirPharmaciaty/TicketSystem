from pydantic import BaseModel


class TicketNoteCreate(BaseModel):
    ticket_id: int
    note: str