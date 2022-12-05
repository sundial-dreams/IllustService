from pixivpy3 import *
import json

from utils.downloader import downloader

from utils.fetcher import fetchIllustsByUser, fetchUserDetail, fetchIllustByRelated, fetchRelatedUsers, \
    fetchFollowingUsers

api = AppPixivAPI()

api.auth(refresh_token='Nte_fDntU17mZchamKsIn96IAt-Hj0QcVpuksoNocc0')

user_id = 13651304

my_user_id = 59189548

illust_id = 103124668


# json_result = api.illust_ranking('day')
#
# print(json_result.illusts)

# r = fetchIllustsByUser(api, 13651304)
# print(r)

# downloader(api, json_result.illusts)

r = fetchUserDetail(api, user_id)
print(r)


def saveMyFollowingUsers():
    users = fetchFollowingUsers(api, my_user_id)
    with open('./data/my_following_user.json', 'w+', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False)


if __name__ == "__main__":
    # saveMyFollowingUsers()
    pass