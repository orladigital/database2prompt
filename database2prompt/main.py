from database2prompt.database.core.database_factory import DatabaseFactory
from database2prompt.database.processing.database_processor import DatabaseProcessor

def main():
    database = "pgsql"
    strategy = DatabaseFactory.run(database)

    next(strategy.connection())
    print("Connected to the database!")

    # tables = strategy.list_tables()
    # print("tables: ", tables)
    
    # estimated_rows = strategy.estimated_rows(tables)
    # print("Estimated_rows:", estimated_rows)
    
    database_processor = DatabaseProcessor(strategy)
    database_processor.process_data()

    # generator = MarkdownGenerator()
    # generated_markdown = generator.generate(tables, estimated_rows)

    # output_file = "dist/output.md"
    # with open(output_file, "w") as file:
    #     file.write(generated_markdown)

    # print(f"Markdown file generated: {output_file}")


if __name__ == "__main__":
    main()
