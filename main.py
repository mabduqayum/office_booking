import sys

from config.config import DatabaseConfig
from src.cmd.cli import BookingSystemCLI


def main() -> None:
    try:
        db_config = DatabaseConfig.from_yaml()
        cli = BookingSystemCLI(db_config)
        cli.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
