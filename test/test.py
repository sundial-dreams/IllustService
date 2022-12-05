import base64

import _md5
import datetime
import random
from datetime import datetime, timezone, timedelta
import hashlib

import jwt

def take_refresh_token(user) -> str:
    token = 'refresh_token:' + str(user.get('_id')) + str(random.randint(0, 1000)) \
        + str(datetime.datetime.now())

    md5 = hashlib.md5()

    md5.update(token.encode(encoding='utf-8'))

    return base64.b64encode(md5.hexdigest().encode(encoding='utf-8'))

def take_token(uid) -> str:
    expires_at = datetime.now(tz=timezone.utc) + timedelta(hours=3)

    return jwt.encode(payload={
        'uid': uid,
        'exp': expires_at
    }, key='secret-illusts'), expires_at

if __name__ == '__main__':
    token, exp = take_token(123)
    print(token)
    print(jwt.decode(token, algorithms='HS256', key='secret-illusts'))
