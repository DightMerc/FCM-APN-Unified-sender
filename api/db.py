from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)


async def connect_mongodb(srv: str, database_name: str) -> AsyncIOMotorClient:
    db = None
    try:
        client = AsyncIOMotorClient(srv)
        db = client[database_name]
        await db.command("buildinfo")  # prevent cold start
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")
    return db
