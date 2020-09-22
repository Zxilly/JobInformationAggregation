from fastapi import FastAPI, Query

from func import *

app = FastAPI()


@app.get('/')
def errorHandler():
    return ['Nothing Here']


@app.get('/login/code')
def loginCode(
        userID: str = Query(...)
):
    return getLoginCode(userID)


@app.get('/login/auth')
def auth(
        userID: str = Query(...)
):
    return checkAuth(userID)
