from pprint import pprint

from sanic import Request, HTTPResponse, Blueprint
from sanic.response import json, SanicException
from service.utils.utils import toIllustUri
from pymongo.database import Database, Collection

query = Blueprint('Query', version=1, url_prefix='query')


# /v1/api/illust?illust_id=1
@query.get('/illust')
async def illust_handler(request: Request) -> HTTPResponse:
    illust_id = request.args.get('illust_id', None)
    if illust_id is None:
        return SanicException(message='illust_id is none')

    uid = request.ctx.uid

    print('uid = ', uid)

    illust_collection: Collection = request.app.ctx.collection.illusts

    result = await illust_collection.find_one({'_id': int(illust_id)})

    if result is None:
        return SanicException(message='illust not found')

    original_type = result.get('original_type')

    return json({
        **result,
        'uri': {
            'large': toIllustUri(illust_id, 'large'),
            'medium': toIllustUri(illust_id, 'medium'),
            'original': toIllustUri(illust_id, 'original', original_type == 'png'),
            'square_medium': toIllustUri(illust_id, 'square_medium'),
        }
    })


@query.get('/all_tags')
async def all_tags_handler(request: Request) -> HTTPResponse:
    return


@query.get('/explore_illusts')
async def explore_illusts_handler(request: Request) -> HTTPResponse:
    app_user_id = request.args.get('app_user_id')


@query.get('/user_profile')
async def user_profile_handler(request: Request) -> HTTPResponse:
    return


@query.get('/illusts_ranking')
async def illusts_ranking_handler(request: Request) -> HTTPResponse:
    return


@query.get('/tags')
async def tags_handler(request: Request) -> HTTPResponse:
    return


@query.get('/trend_tags')
async def trend_tags_handler(request: Request) -> HTTPResponse:
    return


@query.get('/following_user')
async def following_user_handler(request: Request) -> HTTPResponse:
    return


@query.get('/followed_user_illusts')
async def followed_user_illusts_handler(request: Request) -> HTTPResponse:
    return


@query.get('/explore_users')
async def explore_users_handler(request: Request) -> HTTPResponse:
    return


@query.get('/recommended_illusts')
async def recommended_illusts_handler(request: Request) -> HTTPResponse:
    return


@query.get('/test')
async def test_handler(request: Request) -> HTTPResponse:
    return json({
        'status_code': 200,
        'err_no': -1
    })
