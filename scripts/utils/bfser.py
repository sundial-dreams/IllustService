import time

from pixivpy3 import *
from scripts.utils.fetcher import fetchRelatedUsers
from scripts.utils.tools import log

from collections import deque

def bfsRelatedUsers(api: AppPixivAPI, user_ids: list[int]):
    visit_users = dict()
    max_search_deep = 1000

    q = deque()
    for idx in user_ids:
        q.append(idx)
        visit_users.setdefault(idx, True)

    count = 0

    while len(q) and count < max_search_deep:
        print('count = ', count)
        count += 1

        uid = q.popleft()

        related_users = fetchRelatedUsers(api, uid)

        if related_users == -1:
            time.sleep(120)
            log('./logs/related_users_log.txt', str(uid))
            continue

        related_user_ids = list(map(lambda u: u.get('id', None), related_users))

        for r_uid in related_user_ids:
            if not visit_users.get(r_uid, None):
                q.append(r_uid)
                visit_users.setdefault(r_uid, True)

    users = []

    for uid, _ in visit_users.items():
        users.append(uid)

    return users



