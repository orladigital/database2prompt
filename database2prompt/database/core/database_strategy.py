from abc import ABC, abstractmethod
from sqlalchemy import Table

class DatabaseStrategy(ABC):

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def schemas(self):
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

    def list_views(self):
        pass
