from enum import Enum


class TicketStatus(str, Enum):
    NEW = "New"
    ACK = "Acknowledged"
    INP = "In-progress"
    COM = "Completed"
    CAN = "Cancelled"
    REJ = "Rejected"


class TicketOrder(str, Enum):
    OLD = "Oldest"
    LAT = "Latest"
