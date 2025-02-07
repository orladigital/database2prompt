from database2prompt.database.core.database_factory import DatabaseFactory
from database2prompt.database.processing.database_processor import DatabaseProcessor
from database2prompt.markdown.markdown_generator import MarkdownGenerator

def main():
    database = "pgsql"
    strategy = DatabaseFactory.run(database)

    next(strategy.connection())
    print("Connected to the database!")
    
    database_processor = DatabaseProcessor(strategy)
    processed_info = database_processor.process_data()

    generator = MarkdownGenerator(processed_info)
    generated_markdown = generator.generate()

    output_file = "dist/output.md"
    with open(output_file, "w") as file:
        file.write(generated_markdown)

    print(f"Markdown file generated: {output_file}")


if __name__ == "__main__":
    main()
