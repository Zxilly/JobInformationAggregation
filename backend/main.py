import uvicorn
from fastapi import FastAPI, Query

from func import *

app = FastAPI()


@app.get('/')
async def errorHandler():
    return ['Nothing Here']


@app.get('/login/code')
async def loginCode(
        userID: str = Query(...)
):
    return getLoginCode(userID)


@app.get('/login/auth')
async def auth(
        userID: str = Query(...)
):
    return checkLoginAuth(userID)


@app.get('/info')
async def info(
        userID:str = Query(...),
):



if __name__ == '__main__':
    uvicorn.run(app='main:app', debug=True)
