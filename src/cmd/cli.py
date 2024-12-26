from datetime import datetime
import sys
from dataclasses import dataclass

from config.config import DatabaseConfig
from src.utils.constants import DATETIME_FORMAT
from src.models.models import BookingRequest
from src.services.booking import OfficeBookingSystem
from src.repositories.database import Database
from src.services.notification import NotificationManager, EmailService, SMSService
from src.utils.exceptions import BookingSystemError


@dataclass
class UserInput:
    office_number: int
    start_time: datetime
    end_time: datetime
    user_name: str | None = None
    user_email: str | None = None
    user_phone: str | None = None


class BookingSystemCLI:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        self.database = Database(self.db_config)
        self.notification_manager = NotificationManager(
            email_service=EmailService(),
            sms_service=SMSService()
        )
        self.booking_system = OfficeBookingSystem(
            database=self.database,
            notification_manager=self.notification_manager
        )

    def run(self) -> None:
        while True:
            print("\nOffice Booking System")
            print("1. Check office availability")
            print("2. Book an office")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ").strip()

            try:
                match choice:
                    case '1':
                        self.handle_availability_check()
                    case '2':
                        self.handle_booking()
                    case '3' | 'q' | 'quit':
                        self.handle_exit()
                    case _:
                        print("Invalid choice. Please try again.")
            except BookingSystemError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def handle_availability_check(self) -> None:
        user_input = self.get_basic_input()
        result = self.booking_system.check_availability(
            user_input.office_number,
            user_input.start_time,
            user_input.end_time
        )
        print(result)

    def handle_booking(self) -> None:
        user_input = self.get_booking_input()
        booking_request = BookingRequest(
            office_number=user_input.office_number,
            start_time=user_input.start_time,
            end_time=user_input.end_time,
            user_name=user_input.user_name,
            user_email=user_input.user_email,
            user_phone=user_input.user_phone
        )

        result = self.booking_system.book_office(booking_request)
        print(result)

    @staticmethod
    def handle_exit():
        print("Thank you for using the Office Booking System. Goodbye!")
        sys.exit(0)

    def get_basic_input(self) -> UserInput:
        office_number = self.get_office_number()
        start_time = self.get_datetime("Enter start time")
        end_time = self.get_datetime("Enter end time")

        return UserInput(
            office_number=office_number,
            start_time=start_time,
            end_time=end_time
        )

    def get_booking_input(self) -> UserInput:
        basic_input = self.get_basic_input()
        user_name = input("Enter your name: ").strip()
        user_email = input("Enter your email: ").strip()
        user_phone = input("Enter your phone number: ").strip()

        return UserInput(
            office_number=basic_input.office_number,
            start_time=basic_input.start_time,
            end_time=basic_input.end_time,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone
        )

    @staticmethod
    def get_office_number() -> int:
        try:
            return int(input("Enter office number (1-5): "))
        except ValueError:
            raise ValueError("Office number must be a number between 1 and 5")

    @staticmethod
    def get_datetime(prompt: str) -> datetime:
        while True:
            try:
                dt_str = input(f"{prompt} ({DATETIME_FORMAT}): ")
                return datetime.strptime(dt_str, DATETIME_FORMAT)
            except ValueError:
                print(f"Invalid date format. Please use {DATETIME_FORMAT}")
