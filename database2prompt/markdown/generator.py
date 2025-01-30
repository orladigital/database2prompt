def generate_markdown(tables: list[str]):
    """Generates a markdown file given a string value."""

    md_content = "# Table of contents\n"
    for table in tables:
        md_content += f"- {table}\n"
        
    return md_content
