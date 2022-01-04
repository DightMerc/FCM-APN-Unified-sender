import logging

from aiohttp.abc import AbstractAccessLogger

logging_format = (
    "[%(asctime)s.%(msecs)03d][%(module)s.%(funcName)s][%(levelname)s] %(message)s"
)
datefmt = "%Y-%m-%dT%H:%M:%S"


def configure_logging():
    logging.basicConfig(level=logging.INFO, format=logging_format, datefmt=datefmt)


class AccessLogger(AbstractAccessLogger):
    def log(self, request, response, time):
        user_agent = request.headers.get("User-Agent", "")
        self.logger.info(
            f"{request.method} {request.path}"
            f" {response.status} {response.body_length}b {time * 1000:.0f}ms"
            f' "{user_agent}"'
        )
