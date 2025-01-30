from database2prompt.database import connection
from database2prompt.markdown.generator import generate_markdown

def main():
    db = next(connection.get_db())
    print("Connected to the database!")

    tables = connection.list_tables()
    print("tables: ", tables)

    output_file = "database-summary.md"

    generated_markdown = generate_markdown(tables)
    with open(output_file, "w") as file:
        file.write(generated_markdown)
        
    print(f"Markdown file generated: {output_file}")

if __name__ == "__main__":
    main()
