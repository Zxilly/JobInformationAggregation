import base64
import pickle

import requests
from bs4 import BeautifulSoup

from clazz import loginAuth

loginURL = 'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com'
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'}


def save(filename, content):
    with open(f'./data/{filename}.pickle', 'wb') as f:
        pickle.dump(content, f)


def load(filename):
    with open(f'./data/{filename}.pickle', 'rb') as f:
        return pickle.load(f)


def getLoginSession():
    session = requests.session()
    session.headers.update(ua)
    content = session.get(url=loginURL).content.decode()
    htmlTag = BeautifulSoup(content, 'lxml')
    enc = htmlTag.find(id='enc')['value']
    uuid = htmlTag.find(id='uuid')['value']
    print(enc, uuid)
    return session, enc, uuid


def getLoginCode(userID):  # 150s有效期
    session, enc, uuid = getLoginSession()
    # 获取session
    save(userID, {
        'auth': loginAuth(enc, uuid),
        'session': session
    })
    # 写入auth类，写入session
    # 获取图片返回
    loginPicURL = f'https://passport2.chaoxing.com/createqr?uuid={uuid}'
    loginPic = session.get(url=loginPicURL).content
    loginPicBase64 = 'data:image/png;base64,' + base64.b64encode(loginPic).decode()  # 转好DataURL
    return loginPicBase64


def checkLoginAuth(userID):
    pickleObject = load(userID)
    session = pickleObject['session']
    auth = pickleObject['auth']
    return auth.loginAuth(session)
