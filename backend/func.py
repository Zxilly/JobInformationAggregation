import json
import requests


loginURL = 'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com'


def save(filename, content):
    with open(f'./data/{filename}.json', 'w+') as f:
        f.write(json.dumps(content))


def load(filename):
    with open(f'./data.{filename}.json', 'r+') as f:
        return json.loads(f.read())


def getLoginSession(uuid): # 150s有效期
    mainSession = requests.session()
    mainSession.get(url=loginURL)
    loginPic =