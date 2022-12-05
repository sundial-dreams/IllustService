from pymongo import MongoClient

from model.config import CONNECTION, DB_NAME, COLLECTION_ILLUSTS, COLLECTION_USERS, COLLECTION_TAGS, \
    COLLECTION_TRANSLATED_TAGS

client = MongoClient(CONNECTION)

db = client[DB_NAME]

class BaseModel(object):
    def __init__(self, name: str):
        self.collection = db.get_collection(name)

class UsersModel(BaseModel):
    def __init__(self):
        super(UsersModel, self).__init__(COLLECTION_USERS)

class TagsModel(BaseModel):
    def __init__(self):
        super(TagsModel, self).__init__(COLLECTION_TAGS)

class TTagsModel(BaseModel):
    def __init__(self):
        super(TTagsModel, self).__init__(COLLECTION_TRANSLATED_TAGS)

class IllustsModel(BaseModel):
    def __init__(self):
        super(IllustsModel, self).__init__(COLLECTION_ILLUSTS)

