import asyncio
import base64
import pickle
from functools import partial

import requests
from bs4 import BeautifulSoup

# from clazz import *

loginURL = 'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com'
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'}


def save(filename, content):
    with open(f'./data/{filename}.pickle', 'wb') as f:
        pickle.dump(content, f)


def load(filename):
    with open(f'./data/{filename}.pickle', 'rb') as f:
        return pickle.load(f)


def checkXXTConnect():
    req = requests.get(loginURL, headers=ua)
    return req.ok


def getLoginSession():
    session = requests.session()
    session.headers.update(ua)
    content = session.get(url=loginURL).content.decode()
    htmlTag = BeautifulSoup(content, 'lxml')
    enc = htmlTag.find(id='enc')['value']
    uuid = htmlTag.find(id='uuid')['value']
    # print(enc, uuid)
    htmlTag.decompose()
    return session, enc, uuid


def getLoginCode():  # 150s有效期
    session, enc, uuid = getLoginSession()
    # 获取session
    # 写入auth类，写入session
    # 获取图片返回
    loginPicURL = f'https://passport2.chaoxing.com/createqr?uuid={uuid}'
    loginPic = session.get(url=loginPicURL).content
    loginPicBase64 = 'data:image/png;base64,' + base64.b64encode(loginPic).decode()  # 转好DataURL
    cookie = session.cookies.get_dict()
    session.close()
    return loginPicBase64, enc, uuid, cookie


def checkLoginAuth(valid):
    authURL = 'https://passport2.chaoxing.com/getauthstatus'
    with requests.session() as s:
        s.cookies.update(valid.session)
        s.headers.update(ua)
        status = s.post(url=authURL, data={
            'enc': valid.enc,
            'uuid': valid.uuid
        }).json()['status']
        if status:
            return True, s.cookies.get_dict()
        else:
            return False, None


def verify(session: dict):
    verifyURL = "https://mooc2-ans.chaoxing.com/visit/interaction"
    with requests.session() as s:
        s.cookies.update(session)
        s.headers.update(ua)
        redirect = not s.get("https://mooc2-ans.chaoxing.com/visit/interaction", allow_redirects=False).is_redirect
    return redirect


def create_task(coro):
    loop = asyncio.get_running_loop()
    return loop.create_task(coro)


async def getWorkInfo(session: dict):
    allWorkInfo = []
    tasks = []

    s = requests.session()
    s.cookies.update(session)
    s.headers.update(ua)

    lock = asyncio.Lock()

    courseListURL = 'https://mooc2-ans.chaoxing.com/visit/courses/list?rss=1&start=0&size=500&catalogId=0&searchname='

    html = s.get(url=courseListURL).content.decode()
    htmlBS = BeautifulSoup(html, 'lxml')
    for singleCourse in htmlBS.find_all(class_='course-info'):  # 虽然连接是旧版本的，但是解析课程名称和教师名称更方便
        tasks.append(parseOneCourse(singleCourse, s, allWorkInfo, lock))
    htmlBS.decompose()

    print(tasks)

    await asyncio.wait(tasks)

    print("After every Task")
    print(allWorkInfo)

    return allWorkInfo


async def parseOneCourse(singleCourse, s, allWorkInfo, lock):
    courseURL = str(singleCourse.find('a')['href']) + "&ismooc2=1"
    courseName = str(singleCourse.find('span').string)
    teacherName = str(singleCourse.find('p').string)

    # courseHTML = s.get(url=courseURL).content.decode()

    future = asyncio.get_event_loop().run_in_executor(None, partial(s.get, url=courseURL))

    courseHTML = await future

    courseHTMLBS = BeautifulSoup(courseHTML.content.decode(), 'lxml')

    courseWorkURL = str(courseHTMLBS.find('li', dataname="zy-stu").a['data-url']) + '&status=1'

    courseHTMLBS.decompose()

    future = asyncio.get_event_loop().run_in_executor(None, partial(s.get, url=courseWorkURL))

    courseWorkHTML = await future

    courseWorkHTMLBS = BeautifulSoup(courseWorkHTML.content.decode(), 'lxml')

    for oneWork in courseWorkHTMLBS.find_all('li'):
        if oneWork.find('div', class_='icon-zy-g'):
            continue

        # print(courseURL, courseName, teacherName)
        # print(oneWork.prettify())

        workName = str(oneWork.find(class_='fl').string)
        workURL = str(oneWork['data'])

        timeObj = oneWork.find(class_='time')
        if timeObj:
            workTime = str(timeObj.contents[-1]).replace('\r\n', '').strip()
        else:
            workTime = ""

        singleWorkInfo = {
            'courseName': courseName,
            'teacherName': teacherName,
            'workName': workName,
            'workTime': workTime,
            'workURL': workURL
        }
        oneWork.decompose()

        async with lock:
            allWorkInfo.append(singleWorkInfo.copy())

    courseWorkHTMLBS.decompose()

    print("Finish one Task")
