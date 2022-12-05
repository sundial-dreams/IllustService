import json
import os


def read_json(filename) -> dict:
    with open(filename, 'r') as f:
        return json.load(f)

def saved_json(filename, obj):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False)

def log(filename: str, text: str, override=False):
    try:
        if type(text) != str:
            text = str(text)

        if not override:
            with open(filename, 'a+', encoding='utf-8') as f:
                f.writelines(text + '\n')

        else:
            with open(filename, 'w+', encoding='utf-8') as f:
                f.writelines(text)

    except RuntimeError as e:
        print(e)

def read_log(filename: str) -> list[str]:
    if not os.path.exists(filename):
        return -1

    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()
