import hashlib
import random
from datetime import datetime, timezone, timedelta
from sanic import Blueprint, Request, HTTPResponse, exceptions
from sanic.response import SanicException, json
import jwt
from pymongo.collection import Collection
import base64
import json5

from service.utils.utils import take_token, take_uid, take_refresh_token

auth = Blueprint('Authentication', version=1, url_prefix='/auth')


@auth.post('/login')
async def user_login_handler(request: Request) -> HTTPResponse:
    try:
        if request.body is not None:
            body: dict = json5.loads(request.body.decode(encoding='utf-8'))
            data = body.get('data')
        else:
            data = request.form

        email, password = data.get('email'), data.get('password')

        app_users_collection: Collection = request.app.ctx.collection.app_users
        token_collection: Collection = request.app.ctx.collection.token

        app_user = await app_users_collection.find_one({'email': email})

        if app_user is None:
            return json({
                'message': 'User Not Found!',
                'errno': 3
            })

        if app_user.get('password') != password:
            return json({
                'message': 'Password Error!',
                'errno': 4
            })

        uid = str(app_user.get('_id'))
        refresh_token = take_refresh_token(uid)
        access_token, expires_at = take_token(uid)

        await token_collection.insert_one({'token': refresh_token, 'uid': uid})

        return json({
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'expiresAt': expires_at,
            'errno': -1,
        })
    except RuntimeError as e:
        return exceptions.ServerError(message='Server Error!', status_code=500)


@auth.post('/register')
async def user_register_handler(request: Request) -> HTTPResponse:
    try:
        if request.body is not None:
            body: dict = json5.loads(request.body.decode(encoding='utf-8'))
            data = body.get('data')
        else:
            data = request.form

        name, email, password = data.get('name'), data.get('email'), data.get('password')

        app_user_collection: Collection = request.app.ctx.collection.app_users
        token_collection: Collection = request.app.ctx.collection.token

        exist_user = await app_user_collection.find_one({'email': email})

        if exist_user is not None:
            return json({
                'errno': 3,
                'message': 'Email is register!'
            })

        result = await app_user_collection.insert_one({
            'name': name,
            'email': email,
            'password': password,
            'create_date': datetime.now(),
            'avatar': '',
            'background_image_url': '',
            'comment': '',
            'trend_tags': [],
            'followed_users': [],
            'trace_illusts': [],
            'liked_illusts': [],
            'saved_illusts': [],
        })

        if result is None:
            return exceptions.SanicException(message='Register Fail!')

        # uid = str(result.inserted_id)
        #
        # access_token, expires_at = take_token(uid)
        # refresh_token = take_refresh_token(uid)
        #
        # result = await token_collection.insert_one({'token': refresh_token, 'uid': uid})
        #
        # if result is None:
        #     return exceptions.SanicException(message='Refresh token Fail!')

        return json({
            # 'accessToken': access_token,
            # 'expiresAt': expires_at,
            # 'refreshToken': refresh_token,
            'message': 'register success',
            'errno': -1
        })
    except RuntimeError as e:
        return exceptions.ServerError(message='Server Error!', status_code=500)

@auth.post('/refresh_token')
async def refresh_token_handler(request: Request) -> HTTPResponse:
    try:
        if request.body is not None:
            body: dict = json5.loads(request.body.decode(encoding='utf-8'))
            data = body.get('data')
        else:
            data = request.form

        refresh_token = data.get('refresh_token')
        token_collection: Collection = request.app.ctx.collection.token
        result = await token_collection.find_one({'token': refresh_token})

        if result is None:
            return SanicException(message='Invalid token!')

        uid = result.get('uid')

        access_token, expires_at = take_token(uid)

        return json({
            'accessToken': access_token,
            'expiresAt': expires_at
        })

    except RuntimeError as e:
        return SanicException(message='Server Error!', status_code=500)


@auth.post('/logout')
async def user_logout_handler(request: Request) -> HTTPResponse:
    try:
        if request.body is not None:
            body: dict = json5.loads(request.body.decode(encoding='utf-8'))
            data = body.get('data')
        else:
            data = request.form

        refresh_token = data.get('refresh_token')
        uid = request.ctx.uid

        token_collection: Collection = request.app.ctx.collection.token
        result = await token_collection.find_one_and_delete({'token': refresh_token, 'uid': uid})

        if result is None:
            return SanicException(message='Logout fail!')

        return json({
            'errno': -1,
        })

    except RuntimeError as e:
        return exceptions.ServerError(message='Server Error!', status_code=500)
