# database2prompt
An open-source project designed to extract relevant data from databases and transform it into context for Retrieval-Augmented Generation (RAG) in generative AI applications.

## How is it useful?

database2prompt makes it easy to generate prompts for LLM from your database. It reads your PostgreSQL database and generates a markdown containing your database schema, where you will be able to pass as context to a LLM.

## Quick install ⚡

#### Create a enviroment

`python -m venv .venv`

#### Active enviroment 

`source .venv/bin/activate`

#### Install poetry

`pip install poetry`

#### Install dependencies

`poetry install`

#### Start database

`docker compose up -d`

#### Run project

`poetry build`
`poetry run python database2prompt/main.py`

## License

Licensed under the MIT License, see <a href="https://github.com/orladigital/database2prompt/blob/main/LICENSE">LICENSE</a> for more information.
