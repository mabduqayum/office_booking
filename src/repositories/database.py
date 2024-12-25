import sqlite3
from contextlib import contextmanager
from datetime import datetime
from src.utils.constants import DB_NAME
from src.utils.exceptions import DatabaseError
from src.models.models import Occupancy, BookingRequest


class Database:
    def __init__(self, db_name: str = DB_NAME):
        try:
            self.conn = sqlite3.connect(db_name)
            self._create_tables()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to initialize database: {e}")

    @contextmanager
    def transaction(self):
        try:
            yield
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Transaction failed: {e}")

    def _create_tables(self) -> None:
        with self.transaction():
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY,
                    office_number INTEGER,
                    user_name TEXT,
                    user_email TEXT,
                    user_phone TEXT,
                    start_time DATETIME,
                    end_time DATETIME
                )
            ''')

    def is_office_available(self, office_number: int, start_time: datetime, end_time: datetime) -> bool:
        try:
            cursor = self.conn.execute('''
                SELECT 1 FROM bookings
                WHERE office_number = ? AND
                      ((start_time <= ? AND end_time > ?) OR
                       (start_time < ? AND end_time >= ?))
                LIMIT 1
            ''', (office_number, start_time, start_time, end_time, end_time))
            return cursor.fetchone() is None
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to check availability: {e}")

    def get_office_occupancy(self, office_number: int, start_time: datetime):
        try:
            cursor = self.conn.execute('''
                SELECT user_name, start_time, end_time FROM bookings
                WHERE office_number = ? AND start_time <= ? AND end_time > ?
            ''', (office_number, start_time, start_time))
            result = cursor.fetchone()
            return Occupancy(*result) if result else None
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to get occupancy: {e}")

    def book_office(self, booking: BookingRequest) -> None:
        try:
            self.conn.execute('''
                  INSERT INTO bookings (
                      office_number, 
                      user_name, 
                      user_email, 
                      user_phone, 
                      start_time, 
                      end_time
                  )
                  VALUES (?, ?, ?, ?, ?, ?)
              ''', (
                booking.office_number,
                booking.user_name,
                booking.user_email,
                booking.user_phone,
                booking.start_time,
                booking.end_time
            ))
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to book office: {e}")


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
