from enum import Enum
from typing import Final

MAX_OFFICE_NUMBER: Final[int] = 5
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M"

DB_CONFIG: Final[dict] = {
    'dbname': 'office_booking',
    'user': 'admin',
    'password': 'password123',
    'host': 'localhost',
    'port': '5432'
}

class BookingStatus(Enum):
    SUCCESS = "SUCCESS"
    INVALID_OFFICE = "INVALID_OFFICE"
    UNAVAILABLE = "UNAVAILABLE"

class Messages:
    INVALID_OFFICE = "Invalid office number. Please choose between 1 and 5."
    UNAVAILABLE = "The office is not available for the specified time."
    BOOKING_SUCCESS = "Office {} has been successfully booked."
    AVAILABLE = "Office {} is available for booking."
    OCCUPIED = "Office {} is occupied by {} from {} until {}."

    @staticmethod
    def get_booking_message(status: BookingStatus) -> str:
        messages = {
            BookingStatus.SUCCESS: "Booking successful!",
            BookingStatus.INVALID_OFFICE: Messages.INVALID_OFFICE,
            BookingStatus.UNAVAILABLE: Messages.UNAVAILABLE
        }
        return messages.get(status, "An unknown error occurred")
