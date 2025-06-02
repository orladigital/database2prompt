from abc import ABC, abstractmethod
from sqlalchemy import Table
from typing import List, Dict

class DatabaseStrategy(ABC):

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def list_schemas(self) -> List[str]:
        pass

    @abstractmethod
    def list_tables(self, schema_name: str):
        pass

    @abstractmethod
    def estimated_rows(self, tables_name: str):
        pass

    @abstractmethod
    def table_object(self, table: str, schema: str) -> Table:
        pass

    @abstractmethod
    def list_views(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def create_materialized_view(self, query):
        pass

    @abstractmethod
    def get_table_sample(self, table: str, schema: str, limit: int = 5) -> List[Dict]:
        pass
