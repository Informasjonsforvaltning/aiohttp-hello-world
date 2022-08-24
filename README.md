# aiohttp-hello-world

A simple backend service based on [aiohttp](https://docs.aiohttp.org/en/stable/) that can be used as a template.

## Usage

```bash
% curl -i --data '{"name": "John Doe"}' -X POST http://localhost:8000/guests
% curl -i http://localhost:8000/guests
% curl -i http://localhost:8000/guests/3
```

## Develop and run locally

### Requirements

- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Install software

```sh
% git clone https://github.com/stigbd/aiohttp-hello-world.git
% cd aiohttp-hello-world
% pyenv install 3.10.6
% python get-poetry.py
% pipx install nox
% pipx inject nox nox-poetry
% poetry install
```

## Running the API locally

Start the server locally:

```sh
% poetry run adev runserver aiohttp_hello_world
```

## Running the API in a wsgi-server (gunicorn)

```sh
% poetry run gunicorn aiohttp_hello_world:create_app --bind localhost:8000 --worker-class aiohttp.GunicornWebWorker --config=aiohttp_hello_world/gunicorn_config.py
```

## Running the wsgi-server in Docker

To build and run the api in a Docker container:

```sh
% docker build -t digdir/aiohttp-hello-world:latest .
% docker run --env-file .env -p 8000:8000 -d digdir/aiohttp-hello-world:latest
```

The easier way would be with docker-compose:

```sh
docker-compose up --build
```

## Running tests

We use [pytest](https://docs.pytest.org/en/latest/) for contract testing.

To run linters, checkers and tests:

```sh
% nox
```

To run tests with logging, do:

```sh
% nox -s integration_tests -- --log-cli-level=DEBUG
```

## Environment variables

### `LOGGING_LEVEL`

One of the supported levels found [here](https://docs.python.org/3/library/logging.html#levels).
Default: `INFO`

### `CONFIG`

One of

- `dev`: will use fake in-memory data for the database
- `test`: will use fake in-memory data for the database
- `production`: will require and use a monbodb database, cf docker-compose.yml
Default: `production`

An example .env file for local development with use of fake in-memory data:

```sh
LOGGING_LEVEL=DEBUG
CONFIG=dev
```
