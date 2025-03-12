# database2prompt
An open-source project designed to extract relevant data from databases and transform it into context for Retrieval-Augmented Generation (RAG) in generative AI applications.

## How is it useful?

database2prompt makes it easy to generate prompts to LLMS by reading your database and generating a markdown containing in its schema. Therefore, providing context for the AI to maximize the effectiveness of your prompts. 

The project is very simple to use, just follow the quick install tutorial, and once you complete it, you will have a markdown generated at dist/output.md. 

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

## Contribute

You can contribute to database2prompt in many different ways: 

* Suggest a feature
* Code an approved feature idea (you may find them on issues)
* Report a bug
* Fix something and open a pull request
* Help us documenting the code!
* Spreading the word! 
