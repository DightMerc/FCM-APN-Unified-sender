import os

import httpx

from httpx import Response

from api.models import Notification


async def send(notification: Notification) -> Response:
    """
    Send a notification using FCM.

    :param notification: Notification object
    :return: Dictionary containing the result of the request.
    """
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {"Authorization": f"key={os.environ.get('FCM_SERVER_KEY')}"}
    data = {
        "to": notification.token,
        "notification": {
            "title": notification.title,
            "body": notification.body,
            "priority": "high",
        },
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
    return response
