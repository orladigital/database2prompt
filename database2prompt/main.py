from database2prompt.database.core.database_factory import DatabaseFactory
from database2prompt.database.core.database_params import DatabaseParams
from database2prompt.database.core.database_config import DatabaseConfig
from database2prompt.database.processing.database_processor import DatabaseProcessor
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def main():

    config = DatabaseConfig(
    host="localhost",
    port=5432,
    user="admin",
    password="admin",
    database="database_agent",
    schema="public"
    )

    strategy = DatabaseFactory.run("pgsql", config)
    next(strategy.connection())
    print("Connected to the database!")
    
    # Tabelas para documentar
    # tables_to_discovery = ["table_1", "table_2", "table_3"]
    
    # # Tabelas para ignorar
    # tables_to_ignore = ["operacional.xx"]
    
    params = DatabaseParams()
    # params.tables(tables_to_discovery)
    # params.ignore_tables(tables_to_ignore)  # Ignora estas tabelas na documentação

    database_processor = DatabaseProcessor(strategy, params)

    # Generate Markdown
    markdown_content = database_processor.database_to_prompt(output_format="markdown")
    with open("summary-database.md", "w") as file:
        file.write(markdown_content)
    print("Markdown file generated: summary-database.md")

    # Generate JSON
    json_content = database_processor.database_to_prompt(output_format="json")
    with open("summary-database.json", "w", encoding="utf-8") as file:
        json.dump(json_content, file, indent=2, ensure_ascii=False, cls=DateTimeEncoder)
    print("JSON file generated: summary-database.json")

if __name__ == "__main__":
    main()
