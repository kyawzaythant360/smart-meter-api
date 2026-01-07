from app.database import facilitators_collection, usage_collection
from app.auth import hash_password

async def insert_demo_data():
    await facilitators_collection.delete_many({})
    await usage_collection.delete_many({})

    await facilitators_collection.insert_one({
        "name": "facilitator1",
        "hashed_password": hash_password("password123")
    })

    await usage_collection.insert_many([
        {"facilitator_name": "facilitator1", "kilowatts_used": 12.5},
        {"facilitator_name": "facilitator1", "kilowatts_used": 8.3},
    ])
