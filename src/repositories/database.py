import psycopg2
from contextlib import contextmanager
from datetime import datetime

from config.config import DatabaseConfig
from migrations.manager import MigrationManager
from src.utils.exceptions import DatabaseError
from src.models.models import Occupancy, BookingRequest


class Database:
    def __init__(self, db_config: DatabaseConfig):
        try:
            self.db_config = db_config
            self.conn = psycopg2.connect(**db_config.to_dict())
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to initialize database: {e}")

    def _run_migrations(self):
        with MigrationManager(self.db_config) as manager:
            manager.migrate()

    @contextmanager
    def transaction(self):
        try:
            yield
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Transaction failed: {e}")

    def _create_tables(self) -> None:
        with self.transaction():
            with self.conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS bookings (
                        id SERIAL PRIMARY KEY,
                        office_number INTEGER,
                        user_name TEXT,
                        user_email TEXT,
                        user_phone TEXT,
                        start_time TIMESTAMP,
                        end_time TIMESTAMP
                    )
                ''')

    def is_office_available(self, office_number: int, start_time: datetime, end_time: datetime) -> bool:
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    SELECT 1
                    FROM bookings
                    WHERE office_number = %s AND
                          NOT (%s > end_time OR %s > start_time)
                ''', (office_number, start_time, end_time))
                return cur.fetchone() is None
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to check availability: {e}")

    def get_office_occupancy(self, office_number: int, start_time: datetime, end_time: datetime):
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    SELECT user_name, start_time, end_time
                    FROM bookings
                    WHERE office_number = %s AND
                          NOT (%s > end_time OR %s > start_time)
                ''', (office_number, start_time, end_time))
                result = cur.fetchone()
                return Occupancy(*result) if result else None
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to get occupancy: {e}")

    def book_office(self, booking: BookingRequest) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO bookings (
                        office_number, 
                        user_name, 
                        user_email, 
                        user_phone, 
                        start_time, 
                        end_time
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (
                    booking.office_number,
                    booking.user_name,
                    booking.user_email,
                    booking.user_phone,
                    booking.start_time,
                    booking.end_time
                ))
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to book office: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
