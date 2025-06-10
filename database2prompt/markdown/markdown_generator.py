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
                
                column_type = column_data["type"]
                default = column_data["default"] if column_data["default"] != None else ""
                nullable = column_data["nullable"]
                
                md_content += f"    {column_key} {column_type} {default} {nullable},\n"
            md_content += ");\n"
            md_content += "```\n"

            
            if "sample_data" in table_data and table_data["sample_data"]:
                md_content += "\n### Sample Data\n\n"
                md_content += "```sql\n"
                
                headers = list(table_data["sample_data"][0].keys())
                md_content += "| " + " | ".join(headers) + " |\n"
                md_content += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                
                
                for row in table_data["sample_data"]:
                    values = [str(row.get(header, "")) for header in headers]
                    md_content += "| " + " | ".join(values) + " |\n"
                md_content += "```\n"
        
        md_content += "\n"
        md_content += "# Views \n"

        views = self.processed_info["views"]

        for view_key in views.keys():
            md_content += f"- {view_key}\n"

        for view_key in views.keys():
            view = views[view_key]
            
            md_content += "\n"
            md_content += f"## View: {view_key}\n"
            md_content += "\n"
            md_content += "### DDL\n"
            md_content += "```sql\n"
            md_content += f"{view["ddl"]}\n"
            md_content += "```\n"

        return md_content
    
