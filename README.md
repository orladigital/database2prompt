# database2prompt

<div style="width: 100%; display: flex; align-items: center; justify-content: center;">
  
![database2prompt](https://github.com/user-attachments/assets/e6a86262-dc0e-41e4-8983-8e81e60bdef3)

</div>

An open-source project designed to extract relevant data from databases and transform it into context for Retrieval-Augmented Generation (RAG) in generative AI applications.

## How is it useful?

database2prompt makes it easy to generate prompts to LLMS by reading your database and generating a markdown containing its schema. This provides context for the AI to maximize the effectiveness of your prompts.


## Databases Support (WIP)

| Databases    | Support |
|--------------|---------|
| PostgreSQL   | ✅      |

We will add support for most databases including analytical databases


## Output Formats

| Output Format | Support |
|--------------|---------|
| JSON         | ✅      |
| Markdown     | ✅      |

## Example Outputs

You can find example outputs generated by database2prompt in the following files:

- [summary-database.md](summary-database.md) - Example of markdown output
- [summary-database.json](summary-database.json) - Example of JSON output

## Usage

### Installation

```bash
pip install database2prompt
```

### Quick Start

Here's a simple example of how to use database2prompt:

```python
from database2prompt.database.core.database_config import DatabaseConfig
from database2prompt.database.core.database_params import DatabaseParams
from database2prompt.database.core.database_factory import DatabaseFactory
from database2prompt.database.processing.database_processor import DatabaseProcessor
from database2prompt.markdown.markdown_generator import MarkdownGenerator

# 1. Configure database connection
config = DatabaseConfig(
    host="localhost",
    port=5432,
    user="your_user",
    password="your_password",
    database="your_database",
    schema="your_schema"
)

# 2. Connect to database
strategy = DatabaseFactory.run("pgsql", config)
next(strategy.connection())

# 3. Configure which tables to document
params = DatabaseParams()

# Option A: Document specific tables
params.tables(["schema.table1", "schema.table2"])

# Option B: Ignore specific tables
params.ignore_tables(["schema.table_to_ignore"])

# 4. Process database information
database_processor = DatabaseProcessor(strategy, params)

# 5. Generate content to prompt (markdown or json)
content = database_processor.database_to_prompt(output_format="json")

```

### Configuration

Configure the database connection:

```bash
   # .env file
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=postgres
   DB_SCHEMA=public
```

```python
   config = DatabaseConfig.from_env()
```

## Contributing

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/orladigital/database2prompt.git
   cd database2prompt
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install poetry
   poetry install
   ```

4. Start the development database (optional):
   ```bash
   docker compose up -d
   ```

5. Run the project:
   ```bash
   poetry run python database2prompt/main.py
   ```

### How to Contribute

You can contribute to database2prompt in many different ways:

* Suggest a feature
* Code an approved feature idea (check our issues)
* Report a bug
* Fix something and open a pull request
* Help with documentation
* Spread the word!

## License

Licensed under the MIT License, see [LICENSE](https://github.com/orladigital/database2prompt/blob/main/LICENSE) for more information.

