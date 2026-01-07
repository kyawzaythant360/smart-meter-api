import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_URI = os.getenv("MONGO_URI")  # Already includes credentials

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

facilitators_collection = db.facilitators
usage_collection = db.generator_usages
refresh_tokens_collection = db.refresh_tokens
