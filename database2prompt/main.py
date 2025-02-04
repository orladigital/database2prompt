from database2prompt.database import connection
from database2prompt.markdown.generator import generate_markdown

def main():
    next(connection.get_db())
    print("Connected to the database!")

    tables = connection.list_tables()
    print("tables: ", tables)

    generated_markdown = generate_markdown(tables)
    output_file = "dist/output.md"
    with open(output_file, "w") as file:
        file.write(generated_markdown)
        
    print(f"Markdown file generated: {output_file}")

if __name__ == "__main__":
    main()
