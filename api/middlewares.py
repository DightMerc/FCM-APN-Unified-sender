import os
from typing import Awaitable, Callable

from aiohttp import web


@web.middleware
async def access_token_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
):
    access_token = request.headers.get("X-Access-Token")
    if not access_token:
        return web.json_response({"error": "Access token is required"}, status=401)
    if access_token != os.environ["ACCESS_TOKEN"]:
        return web.json_response({"message": "Access denied"}, status=401)
    return await handler(request)
