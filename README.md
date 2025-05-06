# Fastapi web server boilerplate

## Env variables

- `DEBUG` [Optional] - debug mode. `False` by default
- `DEFAULT_LAT`, `DEFAULT_LON`, `DEFAULT_TZ` [Optional] - data for the place you want to look up. Belgrade by default.

## Running

### Option (a) - easy one

`docker-compose up -d`

### Option (b) - not so easy one

From root (here):
- `uvicorn main:app --reload --app-dir app`

### Prerequisites & development

- Install poetry
  - https://python-poetry.org/docs/#installation
- Install dependencies
  - `poetry install`
