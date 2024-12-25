class BookingSystemError(Exception):
    pass

class DatabaseError(BookingSystemError):
    pass

class ValidationError(BookingSystemError):
    pass
