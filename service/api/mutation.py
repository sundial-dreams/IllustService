from sanic import Sanic, Blueprint, Request, HTTPResponse

mutation = Blueprint('Mutation', version=1, url_prefix='mutation')


@mutation.post('/like_illust')
async def like_illust_handler(request: Request) -> HTTPResponse:
    print(request.form)


@mutation.post('/saved_illust')
async def saved_illust_handler(request: Request) -> HTTPResponse:
    print(request.form)


@mutation.post('/follow_user')
async def follow_user_handler(request: Request) -> HTTPResponse:
    print(request.form)


@mutation.post('/search_illusts')
async def search_illusts(request: Request) -> HTTPResponse:
    return
