FROM python:3.11

# Update package lists
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-distutils \
    tesseract-ocr

WORKDIR /code

COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry setuptools wheel
RUN poetry install
CMD ["poetry", "run", "uvicorn", "pebble.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]