from typing import Dict

def generate_markdown(tables: list[str], estimated_rows: Dict[str, int]):
    """Generates a markdown file given a string value."""
    md_content = "# Table of contents\n"
    for table in tables:
        md_content += f"- {table}\n"

    for table in tables:
        md_content += "\n"
        md_content += f"### Table: {table}\n"
        md_content += f"- Estimated rows: {estimated_rows.get(table, 'N/A')}\n"

    return md_content
