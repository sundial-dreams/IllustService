from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, database

COLLECTION_ILLUSTS = 'illusts'

COLLECTION_TAGS = 'tags'

COLLECTION_TTAGS = 'translated_tags'

COLLECTION_USERS = 'users'

COLLECTION_APP_USERS = 'app_users'

COLLECTION_TOKEN = 'token'

class Collections(object):
    def __init__(self, db: database.Database):
        self.db = db
        self.illusts = db.get_collection(COLLECTION_ILLUSTS)
        self.tags = db.get_collection(COLLECTION_TTAGS)
        self.users = db.get_collection(COLLECTION_USERS)
        self.ttags = db.get_collection(COLLECTION_TTAGS)
        self.app_users = db.get_collection(COLLECTION_APP_USERS)
        self.token = db.get_collection(COLLECTION_TOKEN)

async def setup_db() -> (database.Database, Collections):
    client = AsyncIOMotorClient('localhost', 27017)
    db: database.Database = client.illustration
    return db, Collections(db)


