import json
from database2prompt.database.core.database_factory import DatabaseFactory
from database2prompt.database.core.database_params import DatabaseParams
from database2prompt.database.core.database_config import DatabaseConfig
from database2prompt.database.processing.database_processor import DatabaseProcessor
from database2prompt.markdown.markdown_generator import MarkdownGenerator
from database2prompt.json_generator.json_generator import JsonGenerator

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
    processed_info = database_processor.process_data(verbose=False)

    # Generate Markdown
    generator = MarkdownGenerator(processed_info)
    generated_markdown = generator.generate()

    output_file = "summary-database.md"
    with open(output_file, "w") as file:
        file.write(generated_markdown)
    print(f"Markdown file generated: {output_file}")

    # Generate JSON
    json_generator = JsonGenerator(processed_info)
    json_data = json_generator.generate()

    json_output_file = "summary-database.json"
    with open(json_output_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=2, ensure_ascii=False)
    print(f"JSON file generated: {json_output_file}")

if __name__ == "__main__":
    main()
