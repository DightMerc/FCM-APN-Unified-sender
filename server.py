import asyncio
import traceback
import logging

from aiohttp import web

from api.logger import AccessLogger, configure_logging
from api.app import create_app

configure_logging()
logger = logging.getLogger()
runners = []


async def start_app(aiohttp_app: web.Application, address="0.0.0.0", port=5000) -> None:
    runner = web.AppRunner(aiohttp_app, access_log_class=AccessLogger)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()
    logger.info(f"Started aiohttp server on {address}:{port}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    loop.create_task(start_app(app, port=5000))
    try:
        loop.run_forever()
    except Exception:
        logger.error(f"Unexpected exception occurred: {traceback.print_exc()}")
    finally:
        for r in runners:
            loop.run_until_complete(r.cleanup())
