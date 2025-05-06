FROM python:3.12

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock .
COPY pyproject.toml .

COPY ./alembic ./alembic
COPY alembic.ini .
COPY ./tasks ./tasks
COPY ./app .
COPY .version .version

RUN poetry install --no-root

COPY start.sh .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]