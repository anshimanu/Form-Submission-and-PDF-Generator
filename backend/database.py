from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus

# Credentials
USERNAME = "anshimamanu_db_user"
PASSWORD = "Anshima2005"
CLUSTER = "cluster0.hyxymkr"
DB_NAME = "formdb"

MONGO_URI = (
    f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}.mongodb.net/"
    f"{DB_NAME}?retryWrites=true&w=majority"
)

client = AsyncIOMotorClient(MONGO_URI)

db = client[DB_NAME]

async def test_connection():
    try:
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
