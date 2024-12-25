from datetime import datetime
import re


class InputValidator:
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_PATTERN = re.compile(r'^\+?\d{9}$')
    PHONE_NORMALIZE_PATTERN = re.compile(r'[^\d\s+-]')

    @staticmethod
    def validate_office_number(office_number: int) -> str | None:
        if not isinstance(office_number, int):
            return "Office number must be an integer"
        if not 1 <= office_number <= 5:
            return "Office number must be between 1 and 5"
        return None

    @staticmethod
    def validate_datetime(dt: datetime) -> str | None:
        if not isinstance(dt, datetime):
            return "Invalid datetime format"
        if dt < datetime.now():
            return "DateTime cannot be in the past"

    @staticmethod
    def validate_email(email: str) -> str | None:
        if not isinstance(email, str):
            return "Email must be a string"
        if not InputValidator.EMAIL_PATTERN.match(email):
            return "Invalid email address"

    @staticmethod
    def validate_phone(phone: str) -> str | None:
        if not isinstance(phone, str):
            return "Phone number must be a string"
        phone = InputValidator.PHONE_NORMALIZE_PATTERN.sub('', phone)
        if not InputValidator.PHONE_PATTERN.match(phone):
            return "Invalid phone number format. Use only digits, '+', '-', '[:space:]"

    @staticmethod
    def validate_name(name: str) -> str | None:
        if not isinstance(name, str):
            return "Name must be a string"
        if not name.strip():
            return "Name cannot be empty"
        if len(name) < 2:
            return "Name must be at least 2 characters long"
