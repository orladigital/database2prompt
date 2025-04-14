import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"
    schema: str = "public"

    @staticmethod
    def from_env() -> "DatabaseConfig":
        """Create database config from environment variables"""
        load_dotenv()
        
        return DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            database=os.getenv("DB_NAME", "postgres"),
            schema=os.getenv("DB_SCHEMA", "public")
        )
