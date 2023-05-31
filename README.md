# Asdf

## Description

- Download, unzip and process some large XML file (~100MB).
    - I tried to be memory-efficient (don't read the entire file into memory).
    - Ideally only one reading of the file.
- Task 1
    - Total time: ~1.4 sec (~0.85 sec XML processing)
- Task 2
    - Total time: ~1.55 sec (~0.85 sec XML processing)
- Task 3
    - Total time: ~1.7 sec (~0.85 sec XML processing)

## API endpoints

### Local/Dev

- [localhost:8000/1](http://localhost:8000/1)
- [localhost:8000/2](http://localhost:8000/2)
- [localhost:8000/3](http://localhost:8000/3)

### Prod

- [vladadusek.cz/1](https://vladadusek.cz/1)
- [vladadusek.cz/2](https://vladadusek.cz/2)
- [vladadusek.cz/3](https://vladadusek.cz/3)

## Development setup

- [Poetry](https://python-poetry.org/) project.

Install dependencies

```
poetry install
```

Activate current virtual env

```
poetry shell
```

Add dependency

```
poetry add [--group dev] <pypi_package>
```

Run pytest

```
poetry run pytest --verbose --cov
```

Run pylint

```
poetry run pylint asdf/ tests/
```

Run mypy

```
poetry run mypy .
```

Run black

```
poetry run black .
```

Run isort

```
poetry run isort .
```

### Run a development instance

Using Poetry and Uvicorn

```
poetry run dev
```

### Run a production instance

Using Docker and Docker Compose

```
docker build --tag asdf ./
```

```
docker-compose up --detach
```
