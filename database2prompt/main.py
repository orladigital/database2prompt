from database2prompt.database.core.database_factory import DatabaseFactory
from database2prompt.markdown.generator import generate_markdown

def main():
    database = "pgsql"
    strategy = DatabaseFactory.run(database)

    db_strategy = next(strategy.connection())
    print("Connected to the database!")

    tables = strategy.list_tables()
    print("tables: ", tables)

    estimated_rows = strategy.estimated_rows()
    print("Estimated_rows:", estimated_rows)

    output_file = "database-summary.md"

    generated_markdown = generate_markdown(tables)
    with open(output_file, "w") as file:
        file.write(generated_markdown)
        
    print(f"Markdown file generated: {output_file}")

if __name__ == "__main__":
    main()
