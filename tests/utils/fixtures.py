import os
from typing import Dict, Optional

import pytest
from pymongo import MongoClient

db_conn: Optional[MongoClient] = None


@pytest.fixture
def api_url() -> str:
    return "http://0.0.0.0:5000"


@pytest.fixture
def api_headers() -> Dict[str, str]:
    return {"X-Access-Token": os.environ["ACCESS_TOKEN"]}


@pytest.fixture
def db() -> MongoClient:
    global db_conn
    if not db_conn:
        db_conn = MongoClient(os.environ["MONGO_URI"])
    yield db_conn[os.environ["MONGODB_DATABASE"]]
    db_conn.drop_database(os.environ["MONGODB_DATABASE"])
