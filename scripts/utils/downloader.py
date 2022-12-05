import time
import os
from pixivpy3 import *

from tqdm import tqdm


def less(illusts: list, target: int = 10):
    return len(illusts) < 10

def every(callback, arr: list) -> bool:
    for a in arr:
        if not callback(a):
            return False

    return True

def novel_ai(name: str) -> bool:
    name = name.lower().replace(' ', '')
    return name.find('novelai') != -1 or name.find('novalai') != -1


def r18(name: str) -> bool:
    name = name.lower().replace(' ', '')
    return name.find('r18') != -1 or name.find('r-18') != -1


def download_illust(api: AppPixivAPI, name: str, illust_url: str, target_dir: str) -> bool:
    try:
        api.download(illust_url, path=target_dir, name=name)
        return True
    except PixivError as e:
        time.sleep(10)
        return False


def downloader(api: AppPixivAPI, illusts: list, base_dir: str = '../resource') -> (list, list, list):
    if less(illusts):
        return

    downloaded_illusts = []
    downloaded_tags = dict()
    downloaded_translated_tags = dict()

    for illust in tqdm(illusts, desc='download illust', colour='white'):
        illust_type = illust.get('type', None)
        illust_visible = illust.get('visible', None)
        if illust_visible is not None and not illust_visible:
            continue

        if illust_type is not None and illust_type != 'illust':
            continue

        illust_id = illust.get('id', None)

        if illust_id is None:
            continue

        # TODO handle None
        illust_tags = illust.get('tags', [])

        is_novel_ai_or_r18 = False

        for tag_pair in illust_tags:
            name = tag_pair.get('name', None)
            translated_name = tag_pair.get('translated_name', None)

            if name is not None and novel_ai(name) or r18(name):
                is_novel_ai_or_r18 = True
                continue

            if translated_name is not None and novel_ai(translated_name) or r18(name):
                is_novel_ai_or_r18 = True
                continue

        if is_novel_ai_or_r18:
            continue

        illust_square_medium_url = illust.get('image_urls', {}).get('square_medium', None)
        illust_medium_url = illust.get('image_urls', {}).get('medium', None)
        illust_large_url = illust.get('image_urls', {}).get('large', None)
        illust_original_url = illust.get('meta_single_page', {}).get('original_image_url', None)

        try:
            if illust_original_url is None:
                meta_pages = illust.get('meta_pages', [])
                if len(meta_pages) > 0:
                    illust_original_url = meta_pages[0].get('image_urls', {}).get('original', None)

        except RuntimeError as e:
            continue

        if illust_large_url is None or illust_square_medium_url is None or illust_medium_url is None:
            continue

        illust_total_view = illust.get('total_view', None)
        illust_total_bookmarks = illust.get('total_bookmarks', None)

        illust_title = illust.get('title', None)

        illust_create_date = illust.get('create_date', None)

        illust_dimension = [
            illust.get('width', None),
            illust.get('height', None),
        ]

        user_id = illust.get('user', {}).get('id', None)

        url_list = [
            ['large', illust_large_url],
            ['medium', illust_medium_url],
            ['square_medium', illust_square_medium_url],
            ['original', illust_original_url]
        ]

        success_download = []
        original_type = 'jpg'

        for target_dir, url in url_list:
            if url is None:
                continue

            suffix = url.split('.')[-1]
            filename = str(illust_id)
            if suffix:
                filename += ('.' + suffix)
                if target_dir == 'original':
                    original_type = suffix

            else:
                filename += '.jpg'
            pathname = os.path.join(base_dir, target_dir)

            if not os.path.exists(os.path.join(pathname, filename)):
                success_download.append(download_illust(api, filename, url, pathname))

        # TODO download success
        if (len(success_download) == 4 and every(lambda x: x == True, success_download)) or len(success_download) == 0:
            downloaded_illusts.append({
                'id': illust_id,
                'tags': illust_tags,
                'total_view': illust_total_view,
                'total_bookmarks': illust_total_bookmarks,
                'title': illust_title,
                'create_date': illust_create_date,
                'dimension': illust_dimension,
                'user_id': user_id,
                'original_type': original_type
            })

            for tag_pair in illust_tags:
                name = tag_pair.get('name', None)
                translated_name = tag_pair.get('translated_name', None)

                if name is not None and translated_name is not None:
                    if downloaded_tags.get(name, None) is None:
                        downloaded_tags.setdefault(name, [illust_id])
                    else:
                        downloaded_tags.get(name).append(illust_id)

                    if downloaded_translated_tags.get(name, None) is None:
                        downloaded_translated_tags.setdefault(translated_name, [illust_id])

                    else:
                        downloaded_translated_tags.get(translated_name).append(illust_id)

        # download fail
        else:
            for target_dir, url in url_list:
                if url is None:
                    continue

                suffix = url.split('.')[-1]
                filename = str(illust_id)
                if suffix:
                    filename += ('.' + suffix)
                else:
                    filename += '.jpg'
                pathname = os.path.join(base_dir, target_dir)

                if os.path.exists(os.path.join(pathname, filename)):
                    os.remove(os.path.join(pathname, filename))

    return downloaded_illusts, downloaded_tags, downloaded_translated_tags
