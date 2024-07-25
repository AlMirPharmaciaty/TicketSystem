from enum import Enum
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=4)
    description: str = Field(min_length=4)


class TicketNoteCreate(BaseModel):
    ticket_id: int
    note: str = Field(min_length=4)


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
