from database2prompt.database.processing.database_processor import DatabaseProcessor
from database2prompt.database.core.database_strategy import DatabaseStrategy

from sqlalchemy import Table, Column
from sqlalchemy.schema import DefaultClause, Computed, Identity
from sqlalchemy.types import VARCHAR, CHAR, INTEGER, BIGINT, NUMERIC, DATE, TIMESTAMP
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from sqlalchemy.dialects.postgresql.types import TSVECTOR
from sqlalchemy.dialects.postgresql.named_types import DOMAIN

from unittest.mock import Mock

def test_processed_info():
    mock_database_strategy = Mock(DatabaseStrategy)
    mock_table = Mock(Table)
    mock_readonly_column_collection = Mock(ReadOnlyColumnCollection)

    mock_database_strategy.schemas.return_value = ["op"]
    mock_database_strategy.list_tables.return_value = ["stock", "employee"]
    mock_database_strategy.estimated_rows.return_value = {}
    mock_database_strategy.table_object.return_value = mock_table

    mock_table.columns = mock_readonly_column_collection
    mock_readonly_column_collection.items.return_value = []

    processor = DatabaseProcessor(mock_database_strategy)
    result = processor.process_data()
    tables = result["tables"]

    assert tables["op.stock"] is not None
    assert tables["op.stock"]["schema"] == "op"
    assert tables["op.stock"]["name"] == "stock"

    assert tables["op.employee"] is not None
    assert tables["op.employee"]["schema"] == "op"
    assert tables["op.employee"]["name"] == "employee"

def test_processed_estimated_rows():
    mock_database_strategy = Mock(DatabaseStrategy)
    mock_table = Mock(Table)
    mock_readonly_column_collection = Mock(ReadOnlyColumnCollection)

    mock_database_strategy.schemas.return_value = ["public"]
    mock_database_strategy.list_tables.return_value = ["stock", "employee", "user"]
    mock_database_strategy.estimated_rows.return_value = { "user": 1, "stock": 203, "employee": 54 }
    mock_database_strategy.table_object.return_value = mock_table

    mock_table.columns = mock_readonly_column_collection
    mock_readonly_column_collection.items.return_value = []

    processor = DatabaseProcessor(mock_database_strategy)
    result = processor.process_data()
    tables = result["tables"]

    assert tables["public.stock"]["estimated_rows"] == 203
    assert tables["public.user"]["estimated_rows"] == 1
    assert tables["public.employee"]["estimated_rows"] == 54


def test_processed_fields_types():
    mock_database_strategy = Mock(DatabaseStrategy)
    mock_table = Mock(Table)
    mock_readonly_column_collection = Mock(ReadOnlyColumnCollection)
    mock_column_varchar = Mock(Column)
    mock_column_char_no_limit = Mock(Column)
    mock_column_char_with_limit = Mock(Column)
    mock_column_integer = Mock(Column)
    mock_column_bigint = Mock(Column)
    mock_column_numeric = Mock(Column)
    mock_column_date = Mock(Column)
    mock_column_timestamp = Mock(Column)
    mock_column_tsvector = Mock(Column)
    mock_column_domain = Mock(Column)
    mock_type_varchar = Mock(VARCHAR)
    mock_type_char_no_limit = Mock(CHAR)
    mock_type_char_with_limit = Mock(CHAR)
    mock_type_integer = Mock(INTEGER)
    mock_type_bigint = Mock(BIGINT)
    mock_type_numeric = Mock(NUMERIC)
    mock_type_date = Mock(DATE)
    mock_type_timestamp = Mock(TIMESTAMP)
    mock_type_tsvector = Mock(TSVECTOR)
    mock_type_domain = Mock(DOMAIN)

    mock_database_strategy.schemas.return_value = ["public"]
    mock_database_strategy.list_tables.return_value = ["user"]
    mock_database_strategy.estimated_rows.return_value = { "user": 1 }
    mock_database_strategy.table_object.return_value = mock_table
    
    mock_table.columns = mock_readonly_column_collection
    mock_readonly_column_collection.items.return_value = [
        ("col0", mock_column_varchar),
        ("col1", mock_column_char_no_limit),
        ("col2", mock_column_char_with_limit),
        ("col3", mock_column_integer),
        ("col4", mock_column_bigint),
        ("col5", mock_column_numeric),
        ("col6", mock_column_date),
        ("col7", mock_column_timestamp),
        ("col8", mock_column_tsvector),
        ("col9", mock_column_domain)
    ]

    mock_column_varchar.type = mock_type_varchar
    mock_column_varchar.server_default = None
    mock_column_varchar.nullable = False
    mock_type_varchar.length = 4

    mock_column_char_no_limit.type = mock_type_char_no_limit
    mock_column_char_no_limit.server_default = None
    mock_column_char_no_limit.nullable = False
    mock_type_char_no_limit.length = None

    mock_column_char_with_limit.type = mock_type_char_with_limit
    mock_column_char_with_limit.server_default = None
    mock_column_char_with_limit.nullable = False
    mock_type_char_with_limit.length = 128

    mock_column_integer.type = mock_type_integer
    mock_column_integer.server_default = None
    mock_column_integer.nullable = False

    mock_column_bigint.type = mock_type_bigint
    mock_column_bigint.server_default = None
    mock_column_bigint.nullable = False

    mock_column_numeric.type = mock_type_numeric
    mock_column_numeric.server_default = None
    mock_column_numeric.nullable = False
    mock_type_numeric.precision = 24
    mock_type_numeric.scale = 5

    mock_column_date.type = mock_type_date
    mock_column_date.server_default = None
    mock_column_date.nullable = False

    mock_column_timestamp.type = mock_type_timestamp
    mock_column_timestamp.server_default = None
    mock_column_timestamp.nullable = False

    mock_column_tsvector.type = mock_type_tsvector
    mock_column_tsvector.server_default = None
    mock_column_tsvector.nullable = False

    mock_column_domain.type = mock_type_domain
    mock_column_domain.server_default = None
    mock_column_domain.nullable = False
    mock_type_domain.schema = "another_schema"
    mock_type_domain.name = "my_domain"

    processor = DatabaseProcessor(mock_database_strategy)
    result = processor.process_data()

    tables = result["tables"]
    user_table = tables['public.user']
    fields = user_table["fields"]

    assert fields["col0"]["type"] == "varchar(4)"
    assert fields["col1"]["type"] == "bpchar"
    assert fields["col2"]["type"] == "bpchar(128)"
    assert fields["col3"]["type"] == "int4"
    assert fields["col4"]["type"] == "int8"
    assert fields["col5"]["type"] == "numeric(24,5)"
    assert fields["col6"]["type"] == "date"
    assert fields["col7"]["type"] == "timestamp"
    assert fields["col8"]["type"] == "tsvector"
    assert fields["col9"]["type"] == "another_schema.my_domain"

def test_processed_fields_default_clause():
    mock_database_strategy = Mock(DatabaseStrategy)
    mock_table = Mock(Table)
    mock_readonly_column_collection = Mock(ReadOnlyColumnCollection)
    mock_column_default = Mock(Column)
    mock_default_clause = Mock(DefaultClause)

    mock_database_strategy.schemas.return_value = ["public"]
    mock_database_strategy.list_tables.return_value = ["user"]
    mock_database_strategy.estimated_rows.return_value = { "user": 1 }
    mock_database_strategy.table_object.return_value = mock_table
    
    mock_table.columns = mock_readonly_column_collection
    mock_readonly_column_collection.items.return_value = [("col0", mock_column_default)]

    mock_column_default.type = Mock(INTEGER)
    mock_column_default.server_default = mock_default_clause
    mock_column_default.nullable = True
    mock_default_clause.arg = 123

    processor = DatabaseProcessor(mock_database_strategy)
    result = processor.process_data()

    tables = result["tables"]
    user_table = tables['public.user']
    fields = user_table["fields"]

    assert fields["col0"]["default"] == "DEFAULT 123"

def test_processed_fields_computed_value():
    mock_database_strategy = Mock(DatabaseStrategy)
    mock_table = Mock(Table)
    mock_readonly_column_collection = Mock(ReadOnlyColumnCollection)
    mock_column_computed_not_persisted = Mock(Column)
    mock_column_computed_persisted = Mock(Column)
    mock_type_computed_not_persisted = Mock(Computed)
    mock_type_computed_persisted = Mock(Computed)

    mock_database_strategy.schemas.return_value = ["public"]
    mock_database_strategy.list_tables.return_value = ["user"]
    mock_database_strategy.estimated_rows.return_value = { "user": 1 }
    mock_database_strategy.table_object.return_value = mock_table
    
    mock_table.columns = mock_readonly_column_collection
    mock_readonly_column_collection.items.return_value = [
        ("col0", mock_column_computed_not_persisted),
        ("col1", mock_column_computed_persisted)
    ]

    mock_column_computed_not_persisted.type = Mock(INTEGER)
    mock_column_computed_not_persisted.server_default = mock_type_computed_not_persisted
    mock_column_computed_not_persisted.nullable = True
    mock_type_computed_not_persisted.sqltext = "({some sql not persisted})"
    mock_type_computed_not_persisted.persisted = False

    mock_column_computed_persisted.type = Mock(INTEGER)
    mock_column_computed_persisted.server_default = mock_type_computed_persisted
    mock_column_computed_persisted.nullable = True
    mock_type_computed_persisted.sqltext = "({another sql but persisted})"
    mock_type_computed_persisted.persisted = True

    processor = DatabaseProcessor(mock_database_strategy)
    result = processor.process_data()

    tables = result["tables"]
    user_table = tables['public.user']
    fields = user_table["fields"]

    assert fields["col0"]["default"] == "GENERATED ALWAYS AS ({some sql not persisted})"
    assert fields["col1"]["default"] == "GENERATED ALWAYS AS ({another sql but persisted}) STORED"

def test_processed_fields_generated_identity():
    mock_database_strategy = Mock(DatabaseStrategy)
    mock_table = Mock(Table)
    mock_readonly_column_collection = Mock(ReadOnlyColumnCollection)
    mock_column_identity_cycle = Mock(Column)
    mock_column_identity_no_cycle = Mock(Column)
    mock_type_identity_cycle = Mock(Identity)
    mock_type_identity_no_cycle = Mock(Identity)

    mock_database_strategy.schemas.return_value = ["public"]
    mock_database_strategy.list_tables.return_value = ["user"]
    mock_database_strategy.estimated_rows.return_value = { "user": 1 }
    mock_database_strategy.table_object.return_value = mock_table
    
    mock_table.columns = mock_readonly_column_collection
    mock_readonly_column_collection.items.return_value = [
        ("col0", mock_column_identity_cycle),
        ("col1", mock_column_identity_no_cycle)
    ]

    mock_column_identity_cycle.type = Mock(INTEGER)
    mock_column_identity_cycle.server_default = mock_type_identity_cycle
    mock_column_identity_cycle.nullable = True
    mock_type_identity_cycle.increment = 1
    mock_type_identity_cycle.minvalue = 2
    mock_type_identity_cycle.maxvalue = 3
    mock_type_identity_cycle.start = 4
    mock_type_identity_cycle.cache = 5
    mock_type_identity_cycle.cycle = True

    mock_column_identity_no_cycle.type = Mock(INTEGER)
    mock_column_identity_no_cycle.server_default = mock_type_identity_no_cycle
    mock_column_identity_no_cycle.nullable = True
    mock_type_identity_no_cycle.increment = 2
    mock_type_identity_no_cycle.minvalue = -5
    mock_type_identity_no_cycle.maxvalue = 10
    mock_type_identity_no_cycle.start = 1
    mock_type_identity_no_cycle.cache = 420
    mock_type_identity_no_cycle.cycle = False

    processor = DatabaseProcessor(mock_database_strategy)
    result = processor.process_data()

    tables = result["tables"]
    user_table = tables['public.user']
    fields = user_table["fields"]

    assert fields["col0"]["default"] == "GENERATED BY DEFAULT AS IDENTITY(INCREMENT BY 1 MINVALUE 2 MAXVALUE 3 START 4 CACHE 5 CYCLE)"
    assert fields["col1"]["default"] == "GENERATED BY DEFAULT AS IDENTITY(INCREMENT BY 2 MINVALUE -5 MAXVALUE 10 START 1 CACHE 420 NO CYCLE)"

def test_processed_fields_nullable():
    mock_database_strategy = Mock(DatabaseStrategy)
    mock_table = Mock(Table)
    mock_readonly_column_collection = Mock(ReadOnlyColumnCollection)
    mock_column_null = Mock(Column)
    mock_column_not_null = Mock(Column)

    mock_database_strategy.schemas.return_value = ["public"]
    mock_database_strategy.list_tables.return_value = ["user"]
    mock_database_strategy.estimated_rows.return_value = { "user": 1 }
    mock_database_strategy.table_object.return_value = mock_table
    
    mock_table.columns = mock_readonly_column_collection
    mock_readonly_column_collection.items.return_value = [
        ("col0", mock_column_null),
        ("col1", mock_column_not_null),
    ]

    mock_column_null.type = Mock(INTEGER)
    mock_column_null.server_default = None
    mock_column_null.nullable = True

    mock_column_not_null.type = Mock(INTEGER)
    mock_column_not_null.server_default = None
    mock_column_not_null.nullable = False

    processor = DatabaseProcessor(mock_database_strategy)
    result = processor.process_data()

    tables = result["tables"]
    user_table = tables['public.user']
    fields = user_table["fields"]

    assert fields["col0"]["nullable"] == "NULL"
    assert fields["col1"]["nullable"] == "NOT NULL"