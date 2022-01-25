import logging
import os
import uuid
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
    cursor = db.notifications.find({}, sort=[("created_at", -1)])
    notifications = await cursor.to_list(length=100)
    content = {"notifications": parse_json(notifications)}
    return web.json_response(content)


@routes.get("/api/v1/notifications/{id}")
async def get_notification(request):
    db: AsyncIOMotorClient = request.app["db"]
    logger.info(f"Try to find notification with id {request.match_info['id']}")
    notification = await db.notifications.find_one({"id": request.match_info["id"]})
    if not notification:
        logger.info(f"Notification with id {request.match_info['id']} not found")
        return web.json_response({"error": "Notification not found"}, status=404)
    content = parse_json(notification)
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
    data["type"] = data["type"].upper()
    notification = Notification(**data)

    response, status = await notifications.send(notification)
    if status != 200:
        notification.status = "failed"
        return web.json_response({"error": response}, status=status)
    elif notification.type == "ANDROID" and response["results"][0].get("error"):
        notification.status = "failed"
        return web.json_response(
            {"error": response["results"][0].get("error")}, status=400
        )
    else:
        notification.status = "sent"
    notification.response = response
    notification.response_status = status
    notification.ios_bundle_id = os.environ.get("APNS_TOPIC")
    notification.created_at = datetime.utcnow()
    notification.id = str(uuid.uuid4())
    inserted_id = (await db.notifications.insert_one(asdict(notification))).inserted_id
    content = parse_json(await db.notifications.find_one({"_id": inserted_id}))
    content["created_at"] = str(content["created_at"]["$date"])
    content["_id"] = str(content["_id"]["$oid"])

    return web.json_response(content)
