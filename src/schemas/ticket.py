from pydantic import BaseModel
from datetime import datetime

from src.schemas.ticketStatus import TicketStatus

class Ticket(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

class TicketDetails(Ticket):
    status: TicketStatus
    user_id: str
    username: str

class TicketCreate(BaseModel):
    title: str
    description: str