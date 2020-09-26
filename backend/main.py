import uvicorn
from fastapi import FastAPI, Body

from clazz import *
from func import *

app = FastAPI()


@app.get('/')
async def errorHandler():
    return ['Nothing Here']

@app.get('/checkRunning')
async def checkRunning():
    return True

@app.get('/login/code')
async def loginCode():
    picBase64, enc, uuid, session = getLoginCode()
    valid = loginValid(enc=enc, uuid=uuid, session=session)

    return {'pic': picBase64, 'valid': valid}


@app.post('/login/auth')
async def auth(
        valid: loginValid = Body(..., embed=True)
):
    status,session = checkLoginAuth(valid)
    return {
        'status':status,
        'session':session
    }


@app.post('/login/verifyCookies')
async def verifyCookies(
        session: dict = Body(..., embed=True)
):
    return verify(session)


@app.post('/info')
async def info(
        session: dict = Body(..., embed=True)
):
    return {'workInfo':getWorkInfo(session)}


if __name__ == '__main__':
    uvicorn.run(app='main:app', debug=True)
