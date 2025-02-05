from abc import ABC, abstractmethod


class DatabaseStrategy(ABC):

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def list_tables(self):
        pass

    @abstractmethod
    def estimated_rows(self, tables_name):
        pass

    def list_views(self):
        pass
