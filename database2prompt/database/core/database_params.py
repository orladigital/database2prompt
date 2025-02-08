from typing import Dict, List


class DatabaseParams:
    def __init__(self):
        self.table_contexts: Dict[str, str] = {}
        self._tables : List[str] = {}

    def table_contexts(self, contexts: Dict[str, str]):
        self.table_contexts = contexts

    def tables(self, tables: List[str]):
        self._tables = tables

    def build(self):
        self
