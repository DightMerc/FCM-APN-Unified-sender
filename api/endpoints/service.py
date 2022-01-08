from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/api/v1/monitoring/status/health")
async def get_healthcheck(request):
    return web.json_response({"status": "ok"})
