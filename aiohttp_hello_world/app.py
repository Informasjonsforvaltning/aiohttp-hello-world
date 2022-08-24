"""Package for exposing validation endpoint."""
import logging
import os
from typing import Any

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware
from dotenv import load_dotenv
import motor.motor_asyncio

from .adapter import FakeRepository, MongoRepository
from .view import Guest, Guests, Ping, Ready

load_dotenv()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
CONFIG = os.getenv("CONFIG", "production")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 27017))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


async def hello(request: web.Request) -> web.Response:
    """Return a friendly HTTP greeting."""
    return web.Response(text="Hello, world")


async def create_app() -> web.Application:
    """Create a web application."""
    app = web.Application(
        middlewares=[
            cors_middleware(allow_all=True),
            error_middleware(),  # default error handler for whole application
        ]
    )
    app.add_routes(
        [
            web.view("/ping", Ping),
            web.view("/ready", Ready),
            web.view("/guests", Guests),
            web.view("/guests/{id}", Guest),
            web.get("/", hello),
        ]
    )

    # logging configurataion:
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)s - %(module)s:%(lineno)d: %(message)s",
        datefmt="%H:%M:%S",
        level=LOGGING_LEVEL,
    )
    logging.getLogger("chardet.charsetprober").setLevel(logging.INFO)

    async def hello_world_context(app: Any) -> Any:
        logging.debug(f"Setting up {CONFIG} context")
        app["BASE_URL"] = BASE_URL

        if CONFIG == "production":  # pragma: no cover
            logging.debug(f"Connecting to db at {DB_HOST}:{DB_PORT}")
            mongo = motor.motor_asyncio.AsyncIOMotorClient(
                host=DB_HOST, port=DB_PORT, username=DB_USER, password=DB_PASSWORD
            )
            db = mongo.DB_NAME
            app["repository"] = MongoRepository(db)
        else:
            app["repository"] = FakeRepository(dict())

        yield

        logging.debug("cleaning up context")
        if CONFIG == "production":  # pragma: no cover
            mongo.close()
        pass

    app.cleanup_ctx.append(hello_world_context)

    return app
