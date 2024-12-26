import argparse
from migrations.manager import MigrationManager


def run_migrations(direction: str = 'up', steps: int = None):
    with MigrationManager() as manager:
        manager.migrate(direction=direction, steps=steps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Database migration tool')
    parser.add_argument('--direction', choices=['up', 'down'], default='up',
                        help='Migration direction (up or down)')
    parser.add_argument('--steps', type=int, help='Number of migrations to roll back')

    args = parser.parse_args()
    run_migrations(direction=args.direction, steps=args.steps)
