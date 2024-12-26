from datetime import datetime
from src.utils.constants import MAX_OFFICE_NUMBER, Messages
from src.models.models import BookingRequest
from src.repositories.database import Database
from src.services.notification import NotificationManager


class OfficeBookingSystem:
    def __init__(self, database: Database, notification_manager: NotificationManager):
        self.db = database
        self.notification_manager = notification_manager

    def check_availability(self, office_number: int, start_time: datetime, end_time: datetime) -> str:
        if not self.is_valid_office_number(office_number):
            return Messages.INVALID_OFFICE

        if self.db.is_office_available(office_number, start_time, end_time):
            return Messages.AVAILABLE.format(office_number)

        occupancy = self.db.get_office_occupancy(office_number, start_time, end_time)
        if occupancy:
            return Messages.OCCUPIED.format(
                office_number,
                occupancy.user_name,
                occupancy.start_time,
                occupancy.end_time
            )
        return Messages.UNAVAILABLE

    def book_office(self, booking_request: BookingRequest) -> str:
        if not self.is_valid_office_number(booking_request.office_number):
            return Messages.INVALID_OFFICE

        occupancy = self.db.get_office_occupancy(booking_request.office_number,
                                                 booking_request.start_time,
                                                 booking_request.end_time)
        if occupancy:
            return Messages.OCCUPIED.format(
                booking_request.office_number,
                occupancy.user_name,
                occupancy.start_time,
                occupancy.end_time
            )

        with self.db.transaction():
            self.db.book_office(booking_request)
            self.notification_manager.send_booking_confirmation(booking_request)

        return Messages.BOOKING_SUCCESS.format(booking_request.office_number)

    @staticmethod
    def is_valid_office_number(office_number: int) -> bool:
        return 1 <= office_number <= MAX_OFFICE_NUMBER
