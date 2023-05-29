# Python 3.10.11
# Debian 11 (bullseye)
FROM python:3.10.11-slim-bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=TRUE

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=TRUE

# Install Debian packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        curl \
        vim \
        gcc \
        python3-dev \
        libpq-dev && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry~=1.4.2

# Create app directory
RUN mkdir /app

# Copy configs inside
COPY pyproject.toml /app/pyproject.toml
COPY poetry.toml /app/poetry.toml
COPY poetry.lock /app/poetry.lock
COPY README.md /app/README.md

# Copy source code & tests inside
COPY asdf /app/asdf
COPY tests /app/tests

WORKDIR /app

# Install Python dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi
