import json
import time
from urllib.parse import unquote

from PIL import Image
# import cv2
from bs4 import BeautifulSoup

# code_url = 'http://passport2.chaoxing.com/createqr?uuid={}&xxtrefer=&type=1&mobiletip=JIA%e6%8e%88%e6%9d%83%e8%af%b7%e6%b1%82'.format(str(uuid.uuid4().hex))

code_html_url = 'http://passport2.chaoxing.com/cloudscanlogin?mobiletip=JIA%e6%8e%88%e6%9d%83%e8%af%b7%e6%b1%82&pcrefer=http://i.chaoxing.com'
headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 (@Kalimdor)_11391565702936108810"
}


def login(conv):
    code_html = conv.get(code_html_url)
    code_html_obj = BeautifulSoup(code_html.content, "html.parser")
    login_uuid = code_html_obj.find(id='uuid')['value']
    login_enc = code_html_obj.find(id='enc')['value']
    code_pic_url = code_html_obj.find(id='ewm')['src']
    # print(login_enc)
    # print(login_uuid)
    code_pic = conv.get('http://passport2.chaoxing.com' + code_pic_url)
    with open('tmp.png', 'wb') as f:
        f.write(code_pic.content)

    img = Image.open('tmp.png')
    img.show()

    # todo: 更好的图片展示方式
    """
    code_pic_show = cv2.imread('tmp.png')
    cv2.imshow('NumCode', code_pic_show)
    cv2.waitKey(0)
    """
    while True:
        login_rec_json = conv.post("http://passport2.chaoxing.com/getauthstatus",
                                   {'uuid': login_uuid, 'enc': login_enc}, headers=headers)
        login_rec_dict = json.loads(login_rec_json.content)
        if login_rec_dict['status'] == True:
            # cv2.destroyAllWindows()
            break
        # print("run once")
        # print(login_rec_dict['status'])
        time.sleep(2)
    return conv


def get_course_list(conv):
    course_list_url_list = []
    course_list_host_url = 'http://mooc1-1.chaoxing.com'
    course_list_url = 'http://mooc1-1.chaoxing.com/visit/courses'

    course_list_html = conv.get(course_list_url, headers=headers)
    html_obj = BeautifulSoup(course_list_html.content, "html.parser")
    course_list_all_tag = html_obj.find_all("h3", class_='clearfix')
    for course_one_tag in course_list_all_tag:
        course_one_tag_info = course_one_tag.find("a")
        # print(course_one_tag_info)
        course_one_tag_url = course_list_host_url + course_one_tag_info.attrs['href'].replace(r"&amp;", r"&")
        # print(course_one_tag_url)
        course_list_url_list.append(course_one_tag_url)
    return course_list_url_list


def get_course_work(conv, course_url_list):
    work_url_list = []
    for course_url in course_url_list:
        host_url = 'http://mooc1-1.chaoxing.com'
        html_content = conv.get(course_url, headers=headers)
        html_obj = BeautifulSoup(str(html_content.content.decode('utf-8').strip()), 'html.parser')
        # print(html_obj)
        # exit(0)
        work_url_quote = html_obj.find("a", string=r'作业  ')['data']
        work_url = unquote(work_url_quote)
        work_url = host_url + work_url
        work_url_list.append(work_url)
        # print(type(work_url))
        # print(work_url)
        # work_html = conv.get(work_url,headers=headers)
    return work_url_list


def get_work_info(conv, url_list):
    work_info_list = []
    for url in url_list:
        html = conv.get(url,headers=headers)
        html_obj = BeautifulSoup(str(html.content),"html.parser")


"""
def backclazzdata(conv):
    course_info_dict = []
    course_info_url = "http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
    course_info = conv.get(course_info_url, headers=headers)
    cdata = json.loads(course_info.content)
    if (cdata['result'] != 1):
        print("课程列表获取失败")
        return 0
    # print(cdata)
    for item in cdata['channelList']:
        if ("course" not in item['content']):
            continue
        pushdata = {}
        pushdata['courseid'] = item['content']['course']['data'][0]['id']
        pushdata['name'] = item['content']['course']['data'][0]['name']
        try:
            pushdata['imgurl'] = item['content']['course']['data'][0]['imageurl']
        except KeyError:
            pushdata['imgurl'] = 'https://p.ananas.chaoxing.com/star3/origin/53cf3d81a310abc6bf2334b3.jpg'
        pushdata['classid'] = item['content']['id']
        course_info_dict.append(pushdata)

    print("获取成功")
    # print(course_info_dict)
    return course_info_dict


# todo: 拿课程信息，抓作业
def gettask(course_info_dict, conv):
    course_list_html_url = 'http://mooc1.jgsu.edu.cn/visit/courses?template=1&s=920e808ee51f050215d0e2b9b41dde26'
    course_list_html = conv.get(course_list_html_url, headers)
    


def show_code_pic():
    print(code_url)
    codepic = conv.get(code_url)
    with open("tmp.png","wb") as f:
        f.write(codepic.content)
    codepic = cv2.imread("tmp.png")
    cv2.imshow("NumCode",codepic)
    cv2.waitKey(0)
    while True:
        conv.get()
"""
