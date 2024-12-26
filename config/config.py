from dataclasses import dataclass
import os
import yaml
from pathlib import Path

@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

    @classmethod
    def from_yaml(cls, environment: str = None) -> 'DatabaseConfig':
        environment = environment or os.getenv('ENV', 'development')
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {config_path}"
            )

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        if environment not in config:
            raise ValueError(
                f"Environment '{environment}' not found in config file"
            )

        db_config = config[environment]['database']
        return cls(
            host=db_config['host'],
            port=int(db_config['port']),
            name=db_config['name'],
            user=db_config['user'],
            password=db_config['password']
        )

    def to_dict(self) -> dict:
        return {
            'host': self.host,
            'port': self.port,
            'database': self.name,
            'user': self.user,
            'password': self.password
        }
