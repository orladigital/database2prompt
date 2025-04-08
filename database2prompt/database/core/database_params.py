from typing import Dict, List, Set


class DatabaseParams:
    def __init__(self):
        self.table_contexts: Dict[str, str] = {}
        self._tables: List[str] = []
        self._ignored_tables: Set[str] = set()

    def table_contexts(self, contexts: Dict[str, str]) -> None:
        """Define table contexts

        Args:
            contexts (Dict[str, str]): Dictionary mapping table names to their contexts
        """
        self.table_contexts = contexts

    def tables(self, tables: List[str]) -> None:
        """Define tables to be documented

        Args:
            tables (List[str]): List of table names to document
        """
        self._tables = tables

    def ignore_tables(self, tables: List[str]) -> None:
        """Define tables to be ignored in documentation

        Args:
            tables (List[str]): List of table names to ignore
        """
        self._ignored_tables.update(tables)

    def should_document_table(self, table_name: str) -> bool:
        """Check if a table should be documented

        Args:
            table_name (str): Name of the table to check

        Returns:
            bool: True if the table should be documented, False otherwise
        """
        if table_name in self._ignored_tables:
            return False
        if not self._tables:  # Se não há tabelas especificadas, documenta todas exceto as ignoradas
            return True
        return table_name in self._tables
