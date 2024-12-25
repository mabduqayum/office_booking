from abc import abstractmethod

from src.models.models import BookingRequest


class NotificationService:
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


class EmailService(NotificationService):
    def send(self, recipient: str, message: str) -> None:
        print(f"Sending email to {recipient}: {message}")


class SMSService(NotificationService):
    def send(self, recipient: str, message: str) -> None:
        print(f"Sending SMS to {recipient}: {message}")


class NotificationManager:
    def __init__(self, email_service: NotificationService, sms_service: NotificationService):
        self.email_service = email_service
        self.sms_service = sms_service

    def send_booking_confirmation(self, booking: BookingRequest) -> None:
        message = (f"You have booked office {booking.office_number} "
                   f"from {booking.start_time} "
                   f"to {booking.end_time}")

        self.email_service.send(booking.user_email, message)
        self.sms_service.send(booking.user_phone, message)
