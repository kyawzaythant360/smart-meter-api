import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DB="smart_meter"
MONGO_URI="mongodb://localhost:27017/mart_meter"


client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

facilitators_collection = db.facilitators
usage_collection = db.generator_usages
refresh_tokens_collection = db.refresh_tokens
