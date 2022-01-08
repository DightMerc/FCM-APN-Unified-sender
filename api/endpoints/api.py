import logging
import os
from dataclasses import asdict
from datetime import datetime
from json import JSONDecodeError

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from api.handlers import notifications
from api.models import Notification
from api.schemas import post_notification
import jsonschema

from api.util import parse_json

logger = logging.getLogger()

routes = web.RouteTableDef()


@routes.get("/api/v1/notifications")
async def get_notifications(request):
    db: AsyncIOMotorClient = request.app["db"]
    cursor = db.notifications.find({})
    notifications = await cursor.to_list(length=100)
    for document in notifications:
        logger.info(document)
    content = {"notifications": parse_json(notifications)}
    return web.json_response(content)


@routes.post("/api/v1/notifications")
async def post_notifications(request):
    db: AsyncIOMotorClient = request.app["db"]
    try:
        data = await request.json()
        jsonschema.validate(data, post_notification())
    except jsonschema.ValidationError as e:
        logger.error(e)
        return web.json_response({"error": e.message}, status=400)
    except JSONDecodeError as e:
        logger.error(e)
        return web.json_response({"error": e.msg}, status=400)
    notification = Notification(**data)

    response, status = await notifications.send(notification)
    if status != 200:
        return web.json_response({"error": response}, status=status)
    elif notification.type == "ANDROID" and response["results"][0].get("error"):
        return web.json_response(
            {"error": response["results"][0].get("error")}, status=400
        )
    else:
        notification.status = "sent"

    notification.response = response
    notification.response_status = status
    notification.ios_bundle_id = os.environ.get("APNS_TOPIC")
    notification.created_at = datetime.utcnow()

    document = asdict(notification)

    await db.notifications.insert_one(document)

    document["created_at"] = datetime.strftime(
        document["created_at"], "%Y-%m-%d %H:%M:%S"
    )
    document["_id"] = str(document["_id"])

    content = {"notification": document}
    return web.json_response(content)
