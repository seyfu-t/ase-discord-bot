FROM python:3.13-slim

# Install essential tools
RUN apt update && apt install -y curl build-essential && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.1

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy essentials for poetry
COPY pyproject.toml ./
COPY LICENSE ./LICENSE

# Copy source code folders
COPY src ./src
COPY scripts ./scripts

# Install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --ansi

# Run
CMD ["python", "src/ase_discord_bot/main.py"]