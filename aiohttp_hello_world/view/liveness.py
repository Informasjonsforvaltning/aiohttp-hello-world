"""Resource module for liveness resources."""
import os

from aiohttp import web
import motor.motor_asyncio

CONFIG = os.getenv("CONFIG", "production")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 27017))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


class Ready(web.View):
    """Class representing ready resource."""

    @staticmethod
    async def get() -> web.Response:
        """Ready route function."""
        if CONFIG in ["development", "test"]:
            pass
        else:  # pragma: no cover
            mongo = motor.motor_asyncio.AsyncIOMotorClient(
                host=DB_HOST, port=DB_PORT, username=DB_USER, password=DB_PASSWORD
            )
            try:
                await mongo.admin.command({"ping": 1})
            except motor.ConnectionFailure as e:
                raise web.HTTPInternalServerError from e

        return web.Response(text="OK")


class Ping(web.View):
    """Class representing ping resource."""

    @staticmethod
    async def get() -> web.Response:
        """Ping route function."""
        return web.Response(text="OK")
