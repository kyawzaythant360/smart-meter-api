import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timedelta
import random

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "energy_db"
COLLECTION_NAME = "usage_collection"

async def seed_data(facilitator_name: str, product_id: str, days: int = 30):
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    product_oid = ObjectId(product_id)
    total_generated = 0

    for day_offset in range(days):
        date_created = datetime.utcnow() - timedelta(days=(days - day_offset))
        generated = random.randint(800, 1500)  # Wh generated that day
        total_generated += generated
        sold = random.randint(200, generated)
        bought = random.randint(50, 300)

        document = {
            "product_id": product_oid,
            "facilitator_name": facilitator_name,
            "dateCreated": date_created,
            "generatedEnergy_wh": generated,
            "generatedEnergyTotal_wh": total_generated,
            "soldEnergy_wh": sold,
            "boughtEnergy_wh": bought
        }

        await collection.insert_one(document)
        print(f"Inserted record for {date_created.date()}")

    print("Seeding complete!")

if __name__ == "__main__":
    # Example usage
    FACILITATOR = "john_doe"
    PRODUCT_ID = "65a8f7c9b7a3f2e8c1234567"  # Replace with your product ObjectId
    asyncio.run(seed_data(FACILITATOR, PRODUCT_ID, days=60))
