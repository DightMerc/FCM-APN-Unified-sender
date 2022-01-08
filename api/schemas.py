from typing import Dict


def post_notification() -> Dict:
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "body": {"type": "string"},
            "token": {"type": "string"},
            "type": {"type": "string"},
        },
        "required": ["title", "body", "token", "type"],
    }
