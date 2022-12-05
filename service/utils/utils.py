import base64
import hashlib
import random
from datetime import datetime, timezone, timedelta
import jwt

host = 'localhost:3030'

secret_key = 'secret-illusts'


def toIllustUri(illust_id, size='large', is_png=False) -> str:
    return host + '/resource/' + size + '/' + str(illust_id) + ('.jpg' if is_png is False else '.png')


def take_token(uid) -> (str, str):
    expires_at = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    return jwt.encode(payload={
        'uid': uid,
        'exp': expires_at
    }, key=secret_key), expires_at.timestamp()


def take_refresh_token(uid) -> str:
    token = 'refresh_token:' + str(uid) + str(random.randint(0, 1000)) \
            + str(datetime.now().timestamp())

    md5 = hashlib.md5()

    md5.update(token.encode(encoding='utf-8'))

    return base64.b64encode(md5.hexdigest().encode(encoding='utf-8')).decode(encoding='utf-8')


def take_uid(email: str) -> str:
    uid = email + str(random.randint(0, 1000)) + str(datetime.now().timestamp())

    md5 = hashlib.md5()

    md5.update(uid.encode(encoding='utf-8'))

    return str(md5.hexdigest())


def decode_token(jwt_token: str) -> dict:
    return jwt.decode(jwt_token, algorithms='HS256', key=secret_key)


if __name__ == '__main__':
    r = take_refresh_token(123)
    print(r)
