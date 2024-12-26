# Office Booking System

## Setup
1. Clone the repository.
2. To start the PostgreSQL database run:
    ```sh
    docker-compose up
    ```
3. To apply database migrations run:
    ```sh
    python ./migrations/migrate.py
    ```

## Usage
Run `python main.py` to start the CLI.

## Testing
Run `python -m unittest discover tests` to run all unit tests.
