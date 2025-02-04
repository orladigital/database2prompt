from database2prompt.database.connection import engine

from typing import Dict
from sqlalchemy import MetaData, Table

def generate_markdown(tables: list[str], estimated_rows: Dict[str, int]):
    """Generates a markdown file given a string value."""

    md_content = "# Contents\n"
    for table in tables:
        md_content += f"- {table}\n"

    for table_name in tables:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        md_content += "\n"
        md_content += f"### Table: {table_name}\n"
        md_content += f"- Estimated rows: {estimated_rows.get(table, 'N/A')}\n"

        md_content += f"## Code\n\n"

        full_qualified_name = f"{table.schema}.{table_name}" if table.schema != None else table_name
        md_content += f"CREATE TABLE {full_qualified_name} (\n"

        for (name, column) in table.columns.items():
            md_content += f"    {name} {column.type}\n"
        md_content += ");\n\n"


        
    return md_content
