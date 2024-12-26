# migrations/manager.py
import os
from typing import List, Tuple, Optional
import psycopg2
from psycopg2.extensions import connection
import logging
from src.utils.exceptions import DatabaseError, MigrationFileError
from config.config import DatabaseConfig

logger = logging.getLogger(__name__)


class MigrationManager:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        self.conn: Optional[connection] = None
        self.migrations_dir = os.path.join(
            os.path.dirname(__file__), 'versions'
        )

    def connect(self) -> None:
        try:
            self.conn = psycopg2.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                database=self.db_config.name,
                user=self.db_config.user,
                password=self.db_config.password
            )
            self._ensure_migrations_table()
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to connect to database: {e}")

    def _ensure_migrations_table(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS migrations (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()

    def get_applied_migrations(self) -> List[str]:
        with self.conn.cursor() as cur:
            cur.execute('SELECT version FROM migrations ORDER BY id DESC')
            return [row[0] for row in cur.fetchall()]

    def _parse_migration_file(self, file_path: str) -> Tuple[str, str]:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            parts = content.split('-- +migrate Down')
            if len(parts) != 2:
                raise MigrationFileError(
                    f"Invalid migration file format: {file_path}"
                )
            up_sql = parts[0].replace('-- +migrate Up', '').strip()
            down_sql = parts[1].strip()
            return up_sql, down_sql
        except IOError as e:
            raise MigrationFileError(f"Failed to read migration file: {e}")

    def migrate(self, direction: str = 'up', steps: Optional[int] = None) -> None:
        try:
            self.connect()
            applied_migrations = self.get_applied_migrations()

            if direction == 'up':
                self._migrate_up(applied_migrations)
            else:
                self._migrate_down(applied_migrations, steps)
        finally:
            self.close()

    def _migrate_up(self, applied_migrations: List[str]) -> None:
        all_migrations = sorted(
            f for f in os.listdir(self.migrations_dir)
            if f.endswith('.up.sql')
        )

        for filename in all_migrations:
            version = filename.replace('.up.sql', '')
            if version not in applied_migrations:
                logger.info(f"Applying migration: {version}")
                migration_path = os.path.join(self.migrations_dir, filename)
                up_sql, _ = self._parse_migration_file(migration_path)
                self._execute_migration(version, up_sql, is_up=True)

    def _migrate_down(
            self,
            applied_migrations: List[str],
            steps: Optional[int]
    ) -> None:
        steps = steps or 1
        migrations_to_rollback = applied_migrations[:steps]

        for version in migrations_to_rollback:
            logger.info(f"Rolling back migration: {version}")
            migration_path = os.path.join(
                self.migrations_dir,
                f"{version}.down.sql"
            )
            _, down_sql = self._parse_migration_file(migration_path)
            self._execute_migration(version, down_sql, is_up=False)

    def _execute_migration(
            self,
            version: str,
            sql: str,
            is_up: bool
    ) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                if is_up:
                    cur.execute(
                        'INSERT INTO migrations (version) VALUES (%s)',
                        (version,)
                    )
                else:
                    cur.execute(
                        'DELETE FROM migrations WHERE version = %s',
                        (version,)
                    )
                self.conn.commit()
                logger.info(
                    f"Successfully {'applied' if is_up else 'rolled back'} "
                    f"migration: {version}"
                )
        except psycopg2.Error as e:
            self.conn.rollback()
            raise DatabaseError(
                f"Failed to {'apply' if is_up else 'roll back'} "
                f"migration {version}: {e}"
            )

    def close(self) -> None:
        if self.conn:
            self.conn.close()
