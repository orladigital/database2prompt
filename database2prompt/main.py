from database2prompt.database import connection
from database2prompt.markdown.generator import generate_markdown

def main():
    db = next(connection.get_db())
    print("Connected to the database!")

    tables = connection.list_tables();
    print("tables: ", tables)

    content = f"""# Metadata information about database
        all tables: {tables}
    """
    output_file = "database-summary.md"

    generate_markdown(content, output_file)
    print(f"Markdown file generated: {output_file}")

if __name__ == "__main__":
    main()
