from database2prompt.database.core.database_factory import DatabaseFactory
from database2prompt.database.core.database_params import DatabaseParams
from database2prompt.database.core.database_config import DatabaseConfig
from database2prompt.database.processing.database_processor import DatabaseProcessor
from database2prompt.markdown.markdown_generator import MarkdownGenerator

def main():
    config = DatabaseConfig(
        host="localhost",
        port=5432,
        user="admin",
        password="admin",
        database="FUNDOS_CER",
        schema="operacional"
    )
    strategy = DatabaseFactory.run("pgsql", config)
    next(strategy.connection())
    print("Connected to the database!")
    
    tables_to_discovery = ["operacional.tb_informacao_diaria", "operacional.tb_fundo_casca", "operacional.tb_casca_classe_subclasse"]
    params = DatabaseParams()
    params.tables(tables_to_discovery)

    database_processor = DatabaseProcessor(strategy, params)
    processed_info = database_processor.process_data(verbose=False)

    generator = MarkdownGenerator(processed_info)
    generated_markdown = generator.generate()

    output_file = "summary-database.md"
    with open(output_file, "w") as file:
        file.write(generated_markdown)

    print(f"Markdown file generated: {output_file}")
if __name__ == "__main__":
    main()
