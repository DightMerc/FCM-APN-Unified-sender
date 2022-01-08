import logging
import os
from typing import Dict, Any

from api.models import Notification

from uuid import uuid4
from aioapns import APNs, NotificationRequest, PushType


logger = logging.getLogger()


async def send(notification: Notification) -> Any:
    """
    Send a notification using APN.

    :param notification: Notification object
    :return: Dictionary containing the result of the request.
    """
    apns_key_client = APNs(
        key=os.path.join(os.getcwd(), "certs", os.environ["APNS_KEY_PATH"]),
        key_id=os.environ["APNS_KEY_ID"],
        team_id=os.environ["APNS_TEAM_ID"],
        topic=os.environ["APNS_TOPIC"],  # Bundle ID
        use_sandbox=False,
    )
    request = NotificationRequest(
        device_token=notification.token,
        message={
            "aps": {
                "alert": {"title": notification.title, "body": notification.body},
                "badge": "1",
            }
        },
        notification_id=str(uuid4()),
        time_to_live=3,
        push_type=PushType.ALERT,
    )
    return await apns_key_client.send_notification(request)
