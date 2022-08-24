FROM python:3.9

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install "poetry==1.1.11"
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ADD aiohttp_hello_world /app/aiohttp_hello_world

EXPOSE 8000

CMD gunicorn "aiohttp_hello_world:create_app"  --config=aiohttp_hello_world/gunicorn_config.py --worker-class aiohttp.GunicornWebWorker
