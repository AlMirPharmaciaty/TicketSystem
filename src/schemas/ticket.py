from pydantic import BaseModel
from datetime import datetime

from src.schemas.ticket_status import TicketStatus


class Ticket(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

class TicketDetails(Ticket):
    status: TicketStatus
    user_id: str
    username: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: TicketStatus


class TicketOrder(str, Enum):
    OLD = "Oldest"
    LAT = "Latest"
