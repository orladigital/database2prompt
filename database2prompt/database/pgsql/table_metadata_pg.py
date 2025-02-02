from sqlalchemy import create_engine, inspect
from database2prompt.database.core.database_strategy import DatabaseStrategy
from sqlalchemy.orm import sessionmaker

class PostgreSQLStrategy(DatabaseStrategy):
    DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/database_agent"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def connection(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def list_tables(self):
        """Return all table names of database"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return tables

    def estimated_rows(self):
        return "10"
