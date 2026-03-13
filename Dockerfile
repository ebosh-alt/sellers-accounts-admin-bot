FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.0.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

WORKDIR /app
COPY . /app


RUN rm -rf /app/.venv \
    && poetry config virtualenvs.create false \
    && poetry config installer.parallel false \
    && poetry install --only main --no-interaction --no-root


CMD ["python", "main.py"]
