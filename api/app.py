import os

from aiohttp import web

from api.db import connect_mongodb

from api.endpoints.service import routes as service_routes
from api.endpoints.api import routes as api_routes
from api.middlewares import access_token_middleware


async def create_app() -> web.Application:
    app = web.Application()
    app["db"] = await connect_mongodb(
        os.environ.get("MONGODB_URI", "mongodb:47017"),
        os.environ.get("MONGODB_DATABASE", "fcm-apn-unified-sender"),
    )

    app.add_routes(api_routes)
    app.add_routes(service_routes)

    app.middlewares.append(access_token_middleware)

    return app
