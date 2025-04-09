from mcp.server.fastmcp import FastMCP
from database2prompt.database.core.database_config import DatabaseConfig
from database2prompt.database.core.database_factory import DatabaseFactory
from typing import Optional

# Create an MCP server
mcp = FastMCP("Database2Prompt")

@mcp.tool()
def connect_database(
    host: str = "localhost",
    port: int = 5432,
    database: str = "database_agent",
    user: str = "admin",
    password: str = "admin",
    schema: Optional[str] = "public"
) -> dict:
    """Connect to a PostgreSQL database using DatabaseFactory"""
    try:
        # Create database configuration
        config = DatabaseConfig(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            schema=schema
        )
        
        # Use DatabaseFactory to create connection
        strategy = DatabaseFactory.run("pgsql", config)
        next(strategy.connection())  # Establish connection
        
        return {
            "status": "success",
            "message": f"Successfully connected to {database} on {host}:{port}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to connect to database: {str(e)}"
        }

if __name__ == "__main__":
    # Run the server in development mode
    mcp.run()
