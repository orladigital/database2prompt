from typing import Dict, List


def generate_markdown(tables: list[str], estimated_rows: Dict[str, int], views: List[Dict[str, str]]):
    """Generates a markdown file given a string value."""
    md_content = "# Table of contents\n"
    for table in tables:
        md_content += f"- {table}\n"

    for table in tables:
        md_content += "\n"
        md_content += f"### Table: {table}\n"
        md_content += f"- Estimated rows: {estimated_rows.get(table, 'N/A')}\n"

    md_content += "\n"
    md_content += "# Views \n"

    for view in views:
        md_content += f"- {view.get("name", "")}\n"

    for views in views:
        md_content += "\n"
        md_content += f"### View: {views.get("name", "")}\n"
        md_content += "\n"
        md_content += "### DDL\n"
        md_content += "```sql\n"
        md_content += f"{views.get("ddl", "")}\n"
        md_content += "```\n"

    return md_content
