from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)

db = client.generator_db
facilitators_collection = db.facilitators
usage_collection = db.generator_usages
refresh_tokens_collection = db.refresh_tokens
