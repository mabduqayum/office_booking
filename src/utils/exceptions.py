class BookingSystemError(Exception):
    pass

class DatabaseError(BookingSystemError):
    pass

class ValidationError(BookingSystemError):
    pass

class MigrationError(Exception):
    pass
# class DatabaseError(MigrationError):
#     pass
class MigrationFileError(MigrationError):
    pass
