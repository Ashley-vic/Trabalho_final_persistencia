from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os

load_dotenv()

DATABASE_URL = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(DATABASE_URL)
db = client.mydatabase
engine = AIOEngine(client=client, database="mydatabase")

def get_engine() -> AIOEngine:
    return engine