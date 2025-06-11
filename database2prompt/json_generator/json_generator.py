import json
from typing import Any, Dict

class DatabaseJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for database objects.
    """
    def default(self, obj: Any) -> Any:
        # Para lidar com todos os possíveis tipos de dados diferentes vindos do sample_data
        try:
            return str(obj)
        except Exception:
            print(f"Error serializing object of type {type(obj)}: {obj}")   
            return None

class JsonGenerator:
    def __init__(self, database_info: dict):
        self.database_info = database_info

    def generate(self) -> Dict:
        """Generate a JSON structure from the database information

        Returns:
            Dict: JSON-compatible dictionary with database structure
        """
        result = {
            "tables": [],
            "views": []
        }

        # Process tables
        for table_name, table_info in self.database_info["tables"].items():
            table_data = {
                "table_name": table_name,
                "schema": table_info["schema"],
                "estimated_rows": table_info["estimated_rows"],
                "columns": [],
                "sample_data": table_info.get("sample_data", [])
            }
            
            # Process columns
            for column_name, column_info in table_info["fields"].items():
                column_data = {
                    "name": column_name,
                    "type": self.format_type(column_info["type"]),
                    "nullable": column_info["nullable"] == "NULL",
                    "default": column_info["default"]
                }
                table_data["columns"].append(column_data)
            
            result["tables"].append(table_data)

        # Process views
        for view_name, view_info in self.database_info["views"].items():
            view_data = {
                "view_name": view_name,
                "schema": view_info["schema"],
                "sql": view_info["ddl"]
            }
            result["views"].append(view_data)

        return result 

    def format_type(self, type: str) -> str:
        if "varchar(None)" in type:
            return "varchar"
        
        return type 