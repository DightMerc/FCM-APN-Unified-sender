from typing import Dict

from api.backends import apn, fcm
from api.models import Notification


async def send(notification: Notification) -> (Dict, int):
    """
    Sends a notification to the device.
    """
    result, status = None, None
    if notification.type == "IOS":
        response = await apn.send(notification)
        result = response.description
        status = 200 if response.is_successful else 400
    elif notification.type == "ANDROID":
        response = await fcm.send(notification)
        result = response.json()
        status = response.status_code

    return result, status
