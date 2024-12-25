from dataclasses import dataclass
from datetime import datetime

@dataclass
class BookingRequest:
    office_number: int
    user_name: str
    user_email: str
    user_phone: str
    start_time: datetime
    end_time: datetime

@dataclass
class Occupancy:
    user_name: str
    start_time: datetime
    end_time: datetime
