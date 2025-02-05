from ..core.database_strategy import DatabaseStrategy

from sqlalchemy import Table
from sqlalchemy.schema import FetchedValue, Computed, Identity, DefaultClause
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy.sql.sqltypes import VARCHAR, INTEGER, BIGINT, NUMERIC, CHAR, DATE, TIMESTAMP
from sqlalchemy.dialects.postgresql.types import TSVECTOR
from sqlalchemy.dialects.postgresql.named_types import DOMAIN

class DatabaseProcessor():
    def __init__(self, database: DatabaseStrategy):
        self.database = database
        self.processed_info = {}

    def process_data(self):
        """Take the information of the database and process it for markdown insertion"""

        self.__iterate_tables(self.database.schemas())

    def __iterate_tables(self, schemas: list[str]):
        for schema_name in schemas:
            tables = self.database.list_tables(schema_name)
            all_estimated_rows = self.database.estimated_rows(tables)

            for table_name in tables:
                table = self.database.table_object(table_name, schema_name)
                fields = self.__get_processed_fields(table)

                self.processed_info[f"{schema_name}.{table_name}"] = {
                    "name": table_name,
                    "schema": schema_name,
                    "estimated_rows": all_estimated_rows.get(table_name),
                    "fields": fields
                }
                print(self.processed_info[f"{schema_name}.{table_name}"], "\n")

    def __get_processed_fields(self, table: Table):
        fields = {}
        for (name, column) in table.columns.items():
            fields[name] = {
                "type": self.__get_processed_type(column.type),
                "default": self.__get_processed_default_value(column.server_default),
                "nullable": self.__get_processed_nullable(column.nullable),
            }
        return fields
    
    def __get_processed_type(self, type: TypeEngine):
        if isinstance(type, VARCHAR):
            return f"varchar({type.length})"
        elif isinstance(type, CHAR):
            return "bpchar" if type.length != None else f"bpchar({type.length})"
        elif isinstance(type, INTEGER):
            return "int4"
        elif isinstance(type, BIGINT):
            return "int8"
        elif isinstance(type, NUMERIC):
            return f"numeric({type.precision}, {type.scale})"
        elif isinstance(type, DATE):
            return "date"
        elif isinstance(type, TIMESTAMP):
            return "timestamp"
        elif isinstance(type, TSVECTOR):
            return "tsvector"
        elif isinstance(type, DOMAIN):
            return f"{type.schema}.{type.name}"
        else:
            raise ValueError(f"Type {type.__class__} not implemented yet")
        
    def __get_processed_default_value(self, default: FetchedValue):
        if default is None: return

        if isinstance(default, DefaultClause):
            return f"DEFAULT {default.arg}"
        elif isinstance(default, Computed):
            return f"GENERATED ALWAYS AS {default.sqltext} {"STORED" if default.persisted else ""}"
        elif isinstance(default, Identity):
            increment_by = f"INCREMENT BY {default.increment}"
            min_value = f"MINVALUE {default.minvalue}"
            max_value = f"MAXVALUE {default.maxvalue}"
            start = f"START {default.start}"
            cache = f"CACHE {default.cache}"
            cycle = "CYCLE" if default.cycle else "NO CYCLE"

            return f"GENERATED BY DEFAULT AS IDENTITY({increment_by} {min_value} {max_value} {start} {cache} {cycle})" 
        else:
            raise ValueError(f"Type {default.__class__} not implemented yet")
        
    def __get_processed_nullable(self, nullable: bool):
        return "NOT NULL" if not nullable else "NULL"

