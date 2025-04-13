import requests
import json

# MCP server URL (assuming default configuration)
SERVER_URL = "http://localhost:8000"

def test_connection(host="localhost", port=5432, database="database_agent", 
                    user="admin", password="admin", schema="public"):
    """Test the connect_database function on the MCP server"""
    payload = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
        "schema": schema
    }
    
    try:
        response = requests.post(
            f"{SERVER_URL}/tools/connect_database",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Connection Result:")
            print(json.dumps(result, indent=2))
            
            if result.get("status") == "success":
                print("\n✅ Successfully connected to the database!")
            else:
                print("\n❌ Failed to connect to the database.")
                print(f"Error: {result.get('message')}")
        else:
            print(f"Server returned status code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to MCP server at {SERVER_URL}")
        print("Make sure the server is running and the URL is correct.")

if __name__ == "__main__":
    print("Testing Database2Prompt MCP Server...\n")
    
    # Test with default parameters
    print("Testing with default parameters:")
    test_connection()
    
    # Test with custom parameters (modify these as needed)
    print("\nTesting with custom parameters:")
    test_connection(
        host="your-postgres-host",
        port=5432,
        database="your-database",
        user="your-username",
        password="your-password",
        schema="your-schema"
    )