# backend/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus

# --- MongoDB Atlas Credentials ---
USERNAME = "anshimamanu_db_user"
PASSWORD = "Anshima2005"  # URL-encode your password here
CLUSTER = "cluster0.hyxymkr"  # Replace with your cluster name
DB_NAME = "formdb"     # Replace with your database name in Atlas

# --- Construct MongoDB Connection URI ---
MONGO_URI = (
    f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}.mongodb.net/"
    f"{DB_NAME}?retryWrites=true&w=majority"
)

# --- Initialize the Client ---
client = AsyncIOMotorClient(MONGO_URI)

# Access the database
db = client[DB_NAME]

# Optional: verify the connection
async def test_connection():
    try:
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)


# from motor.motor_asyncio import AsyncIOMotorClient

# MONGO_URI = "mongodb+srv://anshimamanu_db_user:An%24hima2005@cluster0.hyxymkr.mongodb.net/formdb?appName=Cluster0"

# An%24hima2005

# client = AsyncIOMotorClient(MONGO_URI)
# db = client["formdb"]
# collection = db["submissions"]
