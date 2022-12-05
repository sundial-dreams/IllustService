import time

from pixivpy3 import *
from tqdm import tqdm

from scripts.utils.tools import highQualityCallback, hasError


def fetchIllustsByUser(api: AppPixivAPI, user_id: int, limit=100) -> list:
    try:
        results = api.user_illusts(user_id)
        if results is None:
            time.sleep(120)
            results = api.user_illusts(user_id)
            i = 0

            while results is None and i < 3:
                results = api.user_illusts(user_id)
                time.sleep(120)
                i += 1

            if results is None:
                return -1

        illusts = results.get('illusts', [])

        if len(illusts) == 0:
            return []

        hq_illusts, i = list(filter(highQualityCallback, illusts)), 0

        bar = tqdm(ascii=True, desc='fetch images from user', unit='per')

        bar.update(len(hq_illusts))

        while results.next_url is not None and i < limit:
            next_qs = api.parse_qs(results.next_url)
            results = api.user_illusts(**next_qs)

            illusts = results.get('illusts', [])
            _hq_illust = list(filter(highQualityCallback, illusts))

            hq_illusts += _hq_illust

            i += 1

            bar.update(len(_hq_illust))

        return hq_illusts

    except PixivError as e:
        time.sleep(60)
        return -1


def fetchIllustByRelated(api: AppPixivAPI, illust_id: int, limit=30) -> list:
    try:
        results = api.illust_related(illust_id)
        if results is None:
            time.sleep(120)
            results = api.illust_related(illust_id)
            i = 0

            while results is None and i < 3:
                results = api.illust_related(illust_id)
                time.sleep(120)
                i += 1

            if results is None:
                return -1

        illusts = results.get('illusts', [])

        if len(illusts) == 0:
            return []

        hq_illusts, i = list(filter(highQualityCallback, illusts)), 0

        if len(hq_illusts) == 0:
            return []

        bar = tqdm(ascii=True, desc='fetch illust from related', unit='per')

        bar.update(len(hq_illusts))

        while results.next_url is not None and i < limit:
            next_qs = api.parse_qs(results.next_url)
            results = api.illust_related(**next_qs)
            if results is None:
                return hq_illusts

            illusts = results.get('illusts', [])

            _hq_illusts = list(filter(highQualityCallback, illusts))

            hq_illusts += _hq_illusts

            bar.update(len(_hq_illusts))
            i += 1

        return hq_illusts

    except PixivError as e:
        time.sleep(120)
        return -1


def fetchUserDetail(api: AppPixivAPI, user_id: int) -> dict:
    try:
        results = api.user_detail(user_id)
        if hasError(results):
            time.sleep(120)
            results = api.user_detail(user_id)

            count = 0
            while hasError(results) and count < 3:
                count += 1
                time.sleep(120)
                results = api.user_detail(user_id)

        profile = results.get('profile', {})

        user = results.get('user', None)

        if user is None:
            return {}

        return {
            'id': user.get('id', 0),
            'name': user.get('name', ''),
            'account': user.get('account', ''),
            'avatar': user.get('profile_image_urls', {}).get('medium', ''),
            'comment': user.get('comment', ''),
            'is_followed': user.get('is_followed', False),
            'gender': profile.get('gender', ''),
            'total_illusts': profile.get('total_illusts', 0),
            'background_image_url': profile.get('background_image_url', ''),
        }

    except PixivError as e:
        time.sleep(120)
        return {}


# day week month
def fetchRankingIllusts(api: AppPixivAPI, mode='day', limit=100) -> list:
    try:
        results = api.illust_ranking(mode)
        if results is None:
            return []

        illusts = results.get('illusts', [])

        if len(illusts) == 0:
            return []

        hq_illusts, i = list(filter(highQualityCallback, illusts)), 0

        bar = tqdm(ascii=True, desc='fetch illust from rank list', unit='per')

        bar.update(len(hq_illusts))

        while results.next_url is not None and i < limit:
            next_qs = api.parse_qs(results.next_url)
            results = api.illust_ranking(**next_qs)

            if results is None:
                return hq_illusts

            illusts = results.get('illusts', [])

            if len(illusts) == 0:
                return hq_illusts

            _hq_illusts = list(filter(highQualityCallback, illusts))

            hq_illusts += _hq_illusts

            bar.update(len(_hq_illusts))
            i += 1

        return hq_illusts

    except PixivError as e:
        time.sleep(10)
        return []


def fetchRecommendIllusts(api: AppPixivAPI, limit=100) -> list:
    try:
        results = api.illust_recommended()

        if results is None:
            return []

        illusts = results.get('illusts', [])

        if len(illusts) == 0:
            return []

        hq_illusts, i = list(filter(highQualityCallback, illusts)), 0

        bar = tqdm(ascii=True, desc='fetch illust from recommend', unit='per')

        bar.update(len(hq_illusts))

        while results.next_url is not None and i < limit:
            next_qs = api.parse_qs(results.next_url)
            results = api.illust_recommended(**next_qs)

            if results is None:
                return hq_illusts

            illusts = results.get('illusts', [])

            if len(illusts) == 0:
                return hq_illusts

            _hq_illusts = list(filter(highQualityCallback, illusts))

            hq_illusts += _hq_illusts

            bar.update(len(_hq_illusts))
            i += 1

        return hq_illusts

    except PixivError as e:
        time.sleep(10)
        return []


def fetchIllustsByTag(api: AppPixivAPI, tag: str, limit=200) -> list:
    try:
        results = api.search_illust(tag)

        if results is None:
            return []

        illusts = results.get('illusts', [])

        if len(illusts) == 0:
            return []

        hq_illusts, i = list(filter(highQualityCallback, illusts)), 0

        bar = tqdm(ascii=True, desc='fetch illust from search', unit='per')

        bar.update(len(hq_illusts))

        while results.next_url is not None and i < limit:
            next_qs = api.parse_qs(results.next_url)
            results = api.search_illust(**next_qs)

            if results is None:
                return hq_illusts

            illusts = results.get('illusts', [])

            _hq_illusts = list(filter(highQualityCallback, illusts))

            hq_illusts += _hq_illusts

            i += 1
            bar.update(len(_hq_illusts))

        return hq_illusts

    except PixivError as e:
        time.sleep(10)
        return []


def fetchRelatedUsers(api: AppPixivAPI, user_id: int, limit=10) -> list:
    try:
        results = api.user_related(user_id)
        # print("res = ", results)
        if results is None:
            time.sleep(120)
            results = api.user_related(user_id)

            count = 0
            while results is None and count < 3:
                time.sleep(120)
                count += 1
                results = api.user_related(user_id)

            if results is None:
                return -1

        if hasError(results):
            time.sleep(120)
            results = api.user_related(user_id)
            count = 0

            while hasError(results) and count < 3:
                time.sleep(120)
                count += 1
                results = api.user_related(user_id)

            if hasError(results):
                return -1

        users = results.get('user_previews', [])

        if len(users) == 0:
            return []

        users, i = list(map(lambda user: user.get('user'), users)), 0

        bar = tqdm(ascii=True, desc='fetch user from related', unit='per')

        bar.update(len(users))

        while results.next_url is not None and i < limit:
            next_qs = api.parse_qs(results.next_url)
            results = api.user_related(**next_qs)

            if results is None:
                return users

            _users = results.get('user_previews', [])

            if len(_users) == 0:
                return users

            _users = list(map(lambda user: user.get('user'), _users))

            users += _users

            i += 1

            bar.update(len(_users))

        return users

    except PixivError as e:
        time.sleep(120)
        return -1


def fetchFollowingUsers(api: AppPixivAPI, user_id: int, limit=100) -> list:
    try:
        results = api.user_following(user_id)

        if results is None:
            return []

        users = results.get('user_previews', [])

        if len(users) == 0:
            return []

        users, i = list(map(lambda user: user.get('user'), users)), 0
        bar = tqdm(ascii=True, desc='fetch user from following', unit='per')

        bar.update(len(users))

        while results.next_url is not None and i < limit:
            next_qs = api.parse_qs(results.next_url)
            results = api.user_following(**next_qs)

            if results is None:
                return users

            _users = results.get('user_previews', [])

            if len(_users) == 0:
                return users

            _users = list(map(lambda user: user.get('user'), _users))

            users += _users

            i += 1

            bar.update(len(_users))

        return users

    except PixivError as e:
        time.sleep(10)
        return []
