from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class Notification:
    body: str
    title: str
    token: str
    type: Optional[str] = None
    ios_bundle_id: Optional[str] = None
    created_at: Optional[str] = None
    response: Optional[Dict] = None
    response_status: Optional[int] = None
    status: Optional[str] = None
