from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client: AsyncIOMotorClient = None

async def get_database():
    if Database.client is None:
        raise Exception("Database not initialized")
    return Database.client[settings.database_name]

async def connect_to_mongo():
    try:
        Database.client = AsyncIOMotorClient(settings.mongodb_url)
        # Проверяем подключение
        await Database.client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    if Database.client is not None:
        Database.client.close()
