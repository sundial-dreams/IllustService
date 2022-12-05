import asyncio

from sanic import Sanic
from model.async_mongo import setup_db
import os
from sanic import Request, HTTPResponse, exceptions
from sanic.response import json, SanicException
import jwt

from service.api import api
from service.utils.utils import decode_token
from service.utils.error import no_auth_error, auth_expired_error

app = Sanic('Illust_Service')


@app.before_server_start
async def setup(app: Sanic):
    app.ctx.db, app.ctx.collection = await setup_db()


no_auth_white_lists = {
    '/v1/api/auth/register',
    '/v1/api/auth/login',
    '/v1/api/auth/refresh_token',
    # '/v1/api/query/test',
}

@app.on_request
async def authentication(request: Request):
    if request.path not in no_auth_white_lists:
        # Authorization: Bearer ...
        token = request.token
        if not token:
            return no_auth_error()

        try:
            decoded_token = decode_token(token)
        except jwt.ExpiredSignatureError as e:
            return auth_expired_error(message='Authentication Expired!')

        if not decoded_token:
            return exceptions.Unauthorized(message='Authentication Fail!', status_code=401)
        request.ctx.uid = decoded_token.get('uid')


app.blueprint(api)
