import uvicorn
from fastapi import FastAPI, Body

from clazz import *
from func import *

app = FastAPI()


@app.get('/')
async def errorHandler():
    return ['Nothing Here']


@app.get('/login/code')
async def loginCode():
    picBase64, enc, uuid, session = getLoginCode()
    valid = Valid(enc=enc, uuid=uuid, session=session)

    return {'pic': picBase64, 'valid': valid}


@app.get('/login/auth')
async def auth(
        valid: Valid = Body(..., embed=True)
):
    return checkLoginAuth(valid)


@app.get('/verifyCookie')
async def verifyCookie(
        valid: Valid = Body(..., embed=True)
):
    return verifyCookie(valid)


@app.get('/info')
async def info(
        valid: Valid = Body(..., embed=True)
):
    ...


if __name__ == '__main__':
    uvicorn.run(app='main:app', debug=True)
