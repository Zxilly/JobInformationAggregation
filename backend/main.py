import json
import uuid

from fastapi import FastAPI,Query

app = FastAPI()

@app.get('/')
def errorHandler():
    return ['Nothing Here']

@app.get('/login/code')
def loginCode():
    userId = uuid.uuid1()
    