# database2prompt
An open-source project designed to extract relevant data from databases and transform it into context for Retrieval-Augmented Generation (RAG) in generative AI applications.


# create a enviroment

`python -m venv .venv`

# active enviroment 

`source .venv/bin/activate`

# Install poetry

`pip install poetry`

# Install dependencies

`poetry install`

# Start database

`docker compose up -d`

# Run project

`poetry run python database2prompt/main.py`