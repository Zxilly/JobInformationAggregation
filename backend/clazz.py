from pydantic import BaseModel
import threading

from bs4 import BeautifulSoup


class loginValid(BaseModel):
    enc: str
    uuid: str
    session: dict


threadLock = threading.Lock()


class workThread(threading.Thread):
    def __init__(self, singleCourse, s, allWorkInfo):
        threading.Thread.__init__(self)
        # singleCourse,s,allWorkInfo
        self.singleCourse = singleCourse
        self.s = s
        self.allWorkInfo = allWorkInfo

    def run(self):
        courseURL = 'https://mooc2-ans.chaoxing.com' + str(self.singleCourse.find('a')['href'])
        courseName = str(self.singleCourse.find('span').string)
        teacherName = str(self.singleCourse.find('p').string)
        # print(courseURL,courseName,teacherName)

        courseHTML = self.s.get(url=courseURL).content.decode()
        courseHTMLBS = BeautifulSoup(courseHTML, 'lxml')

        courseWorkURL = str(courseHTMLBS.find('li', dataname="zy-stu").a['data-url']) + '&status=1'

        courseHTMLBS.decompose()
        # print(courseWorkURL)

        courseWorkHTML = self.s.get(courseWorkURL).content.decode()
        courseWorkHTMLBS = BeautifulSoup(courseWorkHTML, 'lxml')

        for oneWork in courseWorkHTMLBS.find_all('li'):
            if oneWork.find('div', class_='icon-zy-g'):
                continue
            workName = oneWork.find(class_='fl').string
            workURL = oneWork['data']
            workTime = str(oneWork.find(class_='time').contents[-1]).replace('\r\n', '').strip()
            singleWorkInfo = {
                'courseName': courseName,
                'teacherName': teacherName,
                'workName': workName,
                'workTime': workTime,
                'workURL': workURL
            }
            # print(singleWorkInfo)
            threadLock.acquire()
            self.allWorkInfo.append(singleWorkInfo.copy())
            threadLock.release()
        courseWorkHTMLBS.decompose()
