from typing import Final

MAX_OFFICE_NUMBER: Final[int] = 5
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M"

class Messages:
    INVALID_OFFICE = "Invalid office number. Please choose between 1 and 5."
    UNAVAILABLE = "The office is not available for the specified time."
    BOOKING_SUCCESS = "Office {} has been successfully booked."
    AVAILABLE = "Office {} is available for booking."
    OCCUPIED = "Office {} is occupied by {} from {} until {}."
