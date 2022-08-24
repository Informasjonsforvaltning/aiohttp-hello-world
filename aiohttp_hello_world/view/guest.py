"""Resource module for hello world resources."""
import json
import logging

from aiohttp import hdrs, web
from multidict import MultiDict

from aiohttp_hello_world.model import GuestModel
from aiohttp_hello_world.service import CreateError, GetError, GuestService


class Guests(web.View):
    """Class representing a collection of hello world resources."""

    async def post(self) -> web.Response:
        """Hello world pst route function."""
        body = await self.request.json()
        repository = self.request.app["repository"]
        logging.debug(f"Got create request for guest {body} of type {type(body)}")
        try:
            data = GuestModel.from_dict(body)
        except KeyError as e:
            raise web.HTTPUnprocessableEntity(
                reason=f"Mandatory property {e.args[0]} is missing."
            ) from e

        try:
            id = await GuestService.create(repository=repository, data=data)
        except CreateError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e

        base_url = self.request.app["BASE_URL"]
        headers = MultiDict([(hdrs.LOCATION, f"{base_url}/guests/{id}")])
        return web.Response(status=201, headers=headers)

    async def get(self) -> web.Response:
        """Hello world get route function."""
        repository = self.request.app["repository"]
        data = await GuestService.get_all(repository=repository)

        data_list = []
        for _d in data:
            data_list.append(_d.to_dict())

        body = json.dumps(data_list, default=str, ensure_ascii=False)
        return web.Response(
            body=body,
            content_type="application/json",
        )


class Guest(web.View):
    """Class representing a hello world resource."""

    async def get(self) -> web.Response:
        """Hello world get route function."""
        repository = self.request.app["repository"]
        id = self.request.match_info["id"]
        try:
            data = await GuestService.get(repository=repository, id=id)
        except GetError as e:
            raise web.HTTPNotFound(reason=str(e)) from e

        body = data.to_json()
        return web.Response(
            body=body,
            content_type="application/json",
        )

    async def head(self) -> web.Response:
        """Hello world head route function."""
        repository = self.request.app["repository"]
        id = self.request.match_info["id"]
        try:
            await GuestService.get(repository=repository, id=id)
        except GetError as e:
            raise web.HTTPNotFound(reason=str(e)) from e

        return web.Response(
            status=200,
            content_type="application/json",
        )

    async def delete(self) -> web.Response:
        """Hello world delete route function."""
        repository = self.request.app["repository"]
        id = self.request.match_info["id"]
        try:
            await GuestService.delete(repository=repository, id=id)
        except GetError as e:
            raise web.HTTPNotFound(reason=str(e)) from e

        return web.Response(status=204)
