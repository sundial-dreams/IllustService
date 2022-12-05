from utils.tools import read_json, saved_json
import os


def append_illusts_for_exist_user():
    users = read_json('./data/users.json')
    illusts = read_json('./data/illusts.json')
    for uid, detail in users.items():
        owner_illusts = []
        for illust_id, illust_detail in illusts.items():
            user_id = illust_detail.get('user_id', None)
            if user_id is not None and int(user_id) == int(uid):
                owner_illusts.append(int(illust_id))
        detail.setdefault('illusts', owner_illusts)

    saved_json('./users.json', users)


def findUserByIllustId(illust_id: int) -> dict:
    users = read_json('./data/users.json')
    illusts = read_json('./data/illusts.json')

    str_illust_id = str(illust_id)

    if illusts.get(str_illust_id, None) is not None:
        uid = illusts.get(str_illust_id).get('user_id', None)
        if uid is not None:
            return users.get(str(uid), None)

    return -1


def findTagsByIllustId(illust_id: int) -> list:
    illusts = read_json('./data/illusts.json')
    str_illust_id = str(illust_id)
    if illusts.get(str_illust_id, None) is not None:
        tags = illusts.get('tags', None)
        if tags is not None:
            return tags


def removeIllustsByUserId(user_id: int) -> None:
    users = read_json('./data/users.json')
    illusts = read_json('./data/illusts.json')
    tags = read_json('./data/tags.json')
    translated_tags = read_json('./data/translated_tags.json')

    base_dir = './illustrations'
    str_user_id = str(user_id)
    dir_list = ['large', 'medium', 'square_medium', 'original']
    illust_ids = users.get(str_user_id, {}).get('illusts', None)

    if illust_ids is not None:
        for illust_id in illust_ids:
            ts = illusts.get(str(illust_id), {}).get('tags', None)

            if ts is not None:
                for name, translated_name in ts:
                    if tags.get(name, None) is not None:
                        tags.get(name).remove(int(illust_id))

                    if translated_tags.get(translated_name, None) is not None:
                        translated_tags.get(translated_name).remove(int(illust_id))

            for d in dir_list:
                filename = os.path.join(base_dir, d, str(illust_id))
                if os.path.exists(filename + '.jpg'):
                    os.remove(filename + '.jpg')

                if os.path.exists(filename + '.png'):
                    os.remove(filename + '.png')

            illusts.pop(str(illust_id))

        users.pop(str_user_id)

    saved_json('./data/users.json', users)
    saved_json('./data/illusts.json', illusts)
    saved_json('./data/tags.json', tags)
    saved_json('./data/translated_tags.json', translated_tags)


if __name__ == "__main__":
    uid = findUserByIllustId(74157206).get('id')
    removeIllustsByUserId(uid)
    print(uid)
