import sys

from src.cmd.cli import BookingSystemCLI


def main() -> None:
    try:
        cli = BookingSystemCLI()
        cli.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
