import time
from pprint import pprint
from pixivpy3 import *
from model.main import UsersModel, TagsModel, TTagsModel, IllustsModel
from tools.tools import read_log
from utils.downloader import downloader
from utils.fetcher import fetchUserDetail, fetchIllustsByUser
from tools.tools import read_json, saved_json, log

api = AppPixivAPI()

api.auth(refresh_token='Nte_fDntU17mZchamKsIn96IAt-Hj0QcVpuksoNocc0')

last_uid_file = '../logs/last_uid.log'
unfetch_user_file = '../logs/unfetch_users.log'

userModel = UsersModel()
tagsModel = TagsModel()
ttagsModel = TTagsModel()
illustsModel = IllustsModel()

def download_from_users():
    count, limit = 0, 1
    user_ids: list = read_json('../data/user_ids.json')
    last_uid = read_log(last_uid_file)

    if last_uid != -1:
        last_uid = int(last_uid[0])
        print('last_uid = ', last_uid)

        i = user_ids.index(last_uid)
        user_ids = user_ids[i + 1: -1]

    for uid in user_ids:

        if count >= limit:
            break

        if userModel.collection.find_one({'_id': int(uid)}):
            continue

        count += 1

        detail = fetchUserDetail(api, uid)
        illusts = fetchIllustsByUser(api, uid)
        print(detail.get("id"), detail.get("name"))

        if illusts == -1:
            time.sleep(120)
            log(unfetch_user_file, uid)

        d_illusts, d_tags, d_translated_tags = downloader(api, illusts)

        if len(d_illusts) == 0:
            continue

        for illust in d_illusts:
            illustsModel.collection.insert_one({
                "_id": int(illust.get('id')),
                **illust
            })

        for tag, illust_ids in d_tags.items():
            illust_ids = list(map(int, illust_ids))
            if tagsModel.collection.find_one({'_id': tag}):
                tagsModel.collection.update_one({'_id': tag}, {'$push': {'illusts': {'$each': illust_ids}}})
            else:
                tagsModel.collection.insert_one({'_id': tag, 'illusts': illust_ids})

        for tag, illust_ids in d_translated_tags.items():
            illust_ids = list(map(int, illust_ids))
            if ttagsModel.collection.find_one({'_id': tag}):
                ttagsModel.collection.update_one({'_id': tag}, {'$push': {'illusts': {'$each': illust_ids}}})
            else:
                ttagsModel.collection.insert_one({'_id': tag, 'illusts': illust_ids})

        userModel.collection.insert_one({
            '_id': int(uid),
            **detail,
            'illusts': list(map(lambda d: int(d.get('id')), d_illusts))
        })

        log(last_uid_file, uid, override=True)


if __name__ == "__main__":
    download_from_users()
