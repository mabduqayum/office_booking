CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    office_number INTEGER,
    user_name TEXT,
    user_email TEXT,
    user_phone TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bookings_office_time
ON bookings (office_number, start_time, end_time);
