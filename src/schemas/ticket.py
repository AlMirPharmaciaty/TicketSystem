from enum import Enum
from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketNoteCreate(BaseModel):
    ticket_id: int
    note: str


class TicketStatus(str, Enum):
    NEW = "New"
    ACK = "Acknowledged"
    INP = "In-progress"
    COM = "Completed"
    CAN = "Cancelled"
    REJ = "Rejected"


class TicketOrder(str, Enum):
    OLD = "Oldest"
    NEW = "Latest"
