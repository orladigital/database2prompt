from sqlite3.dbapi2 import paramstyle

from ..core.database_params import DatabaseParams
from ..core.database_strategy import DatabaseStrategy
from ...markdown.markdown_generator import MarkdownGenerator
from ...json_generator.json_generator import JsonGenerator

from typing import List, Dict, Literal

from sqlalchemy import Table, Boolean
from sqlalchemy.schema import FetchedValue, Computed, Identity, DefaultClause
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy.sql.sqltypes import VARCHAR, INTEGER, BIGINT, NUMERIC, CHAR, DATE, TIMESTAMP, TEXT, DOUBLE_PRECISION
from sqlalchemy.dialects.postgresql.types import TSVECTOR
from sqlalchemy.dialects.postgresql.named_types import DOMAIN

OutputFormat = Literal["json", "markdown"]

class DatabaseProcessor():

    def __init__(self, database: DatabaseStrategy, params: DatabaseParams):
        self.database = database
        self.processed_info = {
            "tables": {},
            "views": {}
        }
        self.params = params

    def database_to_prompt(self, output_format: OutputFormat = "markdown") -> str:
        """Generate documentation from database in the specified format

        Args:
            output_format (str): The output format - either "json" or "markdown"

        Returns:
            str: The generated documentation in the specified format
        """
        # Process database information
        processed_info = self.process_data(verbose=False)

        # Generate output based on format
        if output_format == "markdown":
            generator = MarkdownGenerator(processed_info)
            return generator.generate()
        elif output_format == "json":
            generator = JsonGenerator(processed_info)
            return generator.generate()
        else:
            raise ValueError("Output format must be either 'json' or 'markdown'")

    def process_data(self, verbose: bool = False) -> dict:
        """Take the information of the database and process it for output generation

        Args:
            verbose (bool, optional): If True, prints discovery progress. Defaults to False.
        
        Returns:
            dict: Processed database information
        """
        # Reset processed info to ensure clean state
        self.processed_info = {
            "tables": {},
            "views": {}
        }

        schemas = list(self.database.list_schemas())
        if len(schemas) != 0:
            self.__iterate_tables(schemas, verbose)
        views = self.database.list_views()
        if len(views) != 0:
            self.__iterate_views(views, verbose)
        return self.processed_info

    def __iterate_tables(self, schemas: list[str], verbose: bool = False):
        for schema_name in schemas:
            tables = self.database.list_tables(schema_name)
            all_estimated_rows = self.database.estimated_rows(tables)

            for table_name in tables:
                fully_qualified_name = f"{schema_name}.{table_name}" if schema_name != None else table_name
                
                # Verifica se a tabela deve ser ignorada
                if not self.params.should_document_table(fully_qualified_name):
                    if verbose:
                        print(f"Skipping {fully_qualified_name} table (ignored)...")
                    continue
                
                if verbose:
                    print(f"Discovering {fully_qualified_name} table...")

                table = self.database.table_object(table_name, schema_name)
                fields = self.__get_processed_fields(table)

                self.processed_info["tables"][fully_qualified_name] = {
                    "name": table_name,
                    "schema": schema_name,
                    "estimated_rows": all_estimated_rows.get(table_name),
                    "fields": fields
                }

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
            return "bpchar" if type.length == None else f"bpchar({type.length})"
        elif isinstance(type, INTEGER):
            return "int4"
        elif isinstance(type, BIGINT):
            return "int8"
        elif isinstance(type, NUMERIC):
            return f"numeric({type.precision},{type.scale})"
        elif isinstance(type, DATE):
            return "date"
        elif isinstance(type, TIMESTAMP):
            return "timestamp"
        elif isinstance(type, TSVECTOR):
            return "tsvector"
        elif isinstance(type, DOMAIN):
            return f"{type.schema}.{type.name}"
        elif isinstance(type, TEXT):
            return "text"
        elif isinstance(type, DOUBLE_PRECISION):
            return "double precision"
        else:
            return str(type)

    def __get_processed_default_value(self, default: FetchedValue):
        if default is None: return

        if isinstance(default, DefaultClause):
            return f"DEFAULT {default.arg}"
        elif isinstance(default, Computed):
            return f"GENERATED ALWAYS AS {default.sqltext}{" STORED" if default.persisted else ""}"
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

    def __iterate_views(self, views: List[Dict[str, str]], verbose: bool = False):
        for view in views:
            fully_qualified_name = f"{view["schema"]}.{view["name"]}" if view["schema"] != None else view["name"]
            if verbose:
                print(f"Discovering {fully_qualified_name} view...")
            self.processed_info["views"][fully_qualified_name] = {
                "name": view["name"],
                "schema": view["schema"],
                "ddl": view["ddl"]
            }
