from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/api/v1/notification")
async def get_healthcheck(request):
    return web.json_response({"status": "ok"})
