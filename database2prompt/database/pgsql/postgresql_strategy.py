from typing import Dict, List

from sqlalchemy import create_engine, inspect, text, MetaData, Table
from database2prompt.database.core.database_strategy import DatabaseStrategy
from sqlalchemy.orm import sessionmaker

from database2prompt.database.core.database_strategy import DatabaseStrategy


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

    def schemas(self):
        """Get all schemas of database"""
        inspector = inspect(self.engine)
        return filter(lambda s: s not in ["pg_catalog", "information_schema"], inspector.get_schema_names())

    def list_tables(self, schema_name):
        """Return all table names of database"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names(schema_name)
        return tables

    def estimated_rows(self, tables_name) -> Dict[str, int]:
        query = """
            SELECT relname AS table_name, reltuples::bigint AS estimated_rows
            FROM pg_class
            WHERE relname = ANY(:table_names) 
        """

        with self.engine.connect() as connection:
            result = connection.execute(text(query), {"table_names": tables_name})
            return {row._mapping["table_name"]: row._mapping["estimated_rows"] for row in result}
        
    def table_object(self, table, schema):
        metadata = MetaData()
        return Table(table, metadata, schema=schema, autoload_with=self.engine)
        

    def list_views(self) -> List[Dict[str, str]]:
        query = """
            SELECT schemaname, viewname, definition
            FROM pg_views
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
        """

        views = []
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            for row in result:
                print(f"Schema: {row.schemaname}, View: {row.viewname}\nDefinição:\n{row.definition}\n")
                views.append({"name": row.viewname, "ddl": row.definition})

        return views
