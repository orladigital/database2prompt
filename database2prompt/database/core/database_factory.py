from database2prompt.database.core.database_strategy import DatabaseStrategy
from database2prompt.database.pgsql.postgresql_strategy import PostgreSQLStrategy

class DatabaseFactory:
    strategies = {
        "pgsql": PostgreSQLStrategy
    }

    @staticmethod
    def run(db: str) -> DatabaseStrategy:
        strategy = DatabaseFactory.strategies.get(db)
        if not strategy:
            raise ValueError(f"Database '{db}' not implemented yet")
        return strategy()
