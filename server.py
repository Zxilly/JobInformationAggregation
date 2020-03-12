import asyncio
import json

from aiohttp import web

routes = web.RouteTableDef()

@routes.get('')
async def index(request):
    await asyncio.sleep(0.1)


"""
@routes.get('/json')
async def json1(request):
    await asyncio.sleep(0.1)
    return web.json_response({
        'name': 'anonymous'})


@routes.get('/json/{name}')
async def json2(request):
    await asyncio.sleep(0.1)
    return web.json_response({
        'name': request.match_info['name'] or 'index'})


@routes.get('/hello/')
async def hello1(request):
    await asyncio.sleep(0.1)
    return web.Response(body="<h1>hello user</h1>", headers={'content-type': 'text/html'})


@routes.get('/hello/{name}')
async def hello2(request):
    await asyncio.sleep(0.1)
    return web.Response(body="<h1>hello %s</h1>" % request.match_info['name'], headers={'content-type': 'text/html'})

"""