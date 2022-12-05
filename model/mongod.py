import os

from pymongo import MongoClient
from scripts.utils.tools import read_json

CONNECTION = 'mongodb://localhost:27017/'

DB_NAME = 'illustration'

COLLECTION_ILLUSTS = 'illusts'

COLLECTION_TAGS = 'tags'

COLLECTION_TRANSLATED_TAGS = 'translated_tags'

COLLECTION_USERS = 'users'

client = MongoClient(CONNECTION)

db = client[DB_NAME]

print(client.list_database_names())

if COLLECTION_USERS not in db.list_collection_names():
    db.create_collection(COLLECTION_USERS)

if COLLECTION_ILLUSTS not in db.list_collection_names():
    db.create_collection(COLLECTION_ILLUSTS)

if COLLECTION_TAGS not in db.list_collection_names():
    db.create_collection(COLLECTION_TAGS)

if COLLECTION_TRANSLATED_TAGS not in db.list_collection_names():
    db.create_collection(COLLECTION_TRANSLATED_TAGS)


def insertTags() -> None:
    tags = read_json('./data/tags.json')
    collection = db.get_collection(COLLECTION_TAGS)
    for tag, illusts in tags.items():
        item = {
            "_id": tag,
            "illusts": illusts
        }
        collection.insert_one(item)


def insertUsers() -> None:
    users = read_json('./data/users.json')
    collection = db.get_collection(COLLECTION_USERS)

    for uid, detail in users.items():
        item = {'_id': int(uid)}
        for k, v in detail.items():
            item[k] = v

        collection.insert_one(item)


def insertTranslatedTags() -> None:
    tags = read_json('./data/translated_tags.json')
    collection = db.get_collection(COLLECTION_TRANSLATED_TAGS)
    for tag, illusts in tags.items():
        item = {
            "_id": tag,
            "illusts": illusts
        }
        collection.insert_one(item)


def insertIllusts() -> None:
    illusts = read_json('./data/illusts.json')
    collection = db.get_collection(COLLECTION_ILLUSTS)

    for idx, illust in illusts.items():
        item = {"_id": int(idx)}
        for k, v in illust.items():
            item[k] = v
        collection.insert_one(item)


def addTypeForIllusts() -> None:
    collection = db.get_collection(COLLECTION_ILLUSTS)

    dir_lists = [
        'large',
        'medium',
        'original',
        'square_medium'
    ]

    for files in os.listdir(os.path.join('../resource', 'original')):
        if files.endswith('.jpg') or files.endswith('.png'):
            iid = int(files.split('.')[0])
            if files.endswith('.jpg'):
                collection.update_one({'_id': iid}, {'$set': {'original_type': 'jpg'}})
            else:
                collection.update_one({'_id': iid}, {'$set': {'original_type': 'png'}})


if __name__ == "__main__":
    addTypeForIllusts()
