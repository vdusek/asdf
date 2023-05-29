# Asdf

## API endpoints

### Local

- [localhost:9000/1](http://localhost:9000/1/)
- [localhost:9000/2](http://localhost:9000/2/)
- [localhost:9000/3](http://localhost:9000/3/)

### Prod

- [jakjsmenatom/retailys/1](https://jakjsmenatom/retailys/1/)
- [jakjsmenatom/retailys/2](https://jakjsmenatom/retailys/2/)
- [jakjsmenatom/retailys/3](https://jakjsmenatom/retailys/3/)

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
poetry add [--group dev] pypi_package
```

Run pytest

```
poetry run pytest --verbose --cov
```

Run pylint

```
poetry run pylint jjnt_api/ tests/
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
