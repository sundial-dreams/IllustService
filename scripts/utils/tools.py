import json

def highQualityCallback(value: dict) -> bool:
    return value.get('total_view', 0) >= 3000 and value.get('total_bookmarks', 0) >= 2000 and \
        value.get('type', '') == 'illust'


def read_json(filename) -> dict:
    with open(filename, 'r') as f:
        return json.load(f)

def saved_json(filename, obj):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False)

# {'error': {'user_message': '', 'message': 'Rate Limit', 'reason': '', 'user_message_details': {}}}
def hasError(results: dict) -> bool:
    err = results.get('error', None)
    if err is not None:
        return True

    return False

def log(filename: str, text: str, override=False):
    try:
        if not override:
            with open(filename, 'a+', encoding='utf-8') as f:
                f.writelines(text + '\n')

        else:
            with open(filename, 'w+', encoding='utf-8') as f:
                f.writelines(text)

    except RuntimeError as e:
        print(e)
