class MarkdownGenerator:

    def __init__(self, processed_info: dict):
        self.processed_info = processed_info

    def generate(self):
        """Generates a markdown file given a string value."""

        tables = self.processed_info["tables"]

        md_content = "# Table of contents\n"
        for table_key in tables.keys():
            md_content += f"- {table_key}\n"

        for table_key in tables.keys():
            table_data = tables[table_key]
            md_content += "\n"
            md_content += f"## Table: {table_key}\n"
            md_content += f"- Estimated rows: {table_data["estimated_rows"]}\n"
            md_content += "\n"

            md_content += f"### Code\n\n"

            md_content += "```sql\n"
            full_qualified_name = table_key if table_data["schema"] != None else table_data["name"]
            md_content += f"CREATE TABLE {full_qualified_name} (\n"

            for column_key in table_data["fields"].keys():
                column_data = table_data["fields"][column_key]
                md_content += f"    {column_key} {column_data["type"]} {column_data["default"]} {column_data["nullable"]},\n"
            md_content += ");\n"
            md_content += "```\n"
            
        return md_content
    
