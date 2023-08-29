FROM python:3.11

WORKDIR /code

COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry
RUN poetry install
CMD ["poetry", "run", "uvicorn", "pebble.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]