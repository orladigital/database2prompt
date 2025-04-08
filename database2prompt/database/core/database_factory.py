from typing import Optional
from database2prompt.database.core.database_strategy import DatabaseStrategy
from database2prompt.database.core.database_config import DatabaseConfig
from database2prompt.database.pgsql.postgresql_strategy import PostgreSQLStrategy

class DatabaseFactory:
    strategies = {
        "pgsql": PostgreSQLStrategy
    }

    @staticmethod
    def run(
        db: str,
        config: Optional[DatabaseConfig] = None
    ) -> DatabaseStrategy:
        """Create a database strategy instance

        Args:
            db (str): Database type (e.g. 'pgsql')
            config (Optional[DatabaseConfig], optional): Database configuration.
                If None, will load from environment variables. Defaults to None.

        Returns:
            DatabaseStrategy: Database strategy instance

        Raises:
            ValueError: If database type is not supported
        """
        strategy_class = DatabaseFactory.strategies.get(db)
        if not strategy_class:
            raise ValueError(f"Database '{db}' not implemented yet")
        
        if config is None:
            config = DatabaseConfig.from_env()
            
        return strategy_class(config)
