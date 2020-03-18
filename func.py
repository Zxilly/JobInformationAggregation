import base64
import json
import time

from PIL import Image
# import cv2
from bs4 import BeautifulSoup, SoupStrainer

# code_url = 'http://passport2.chaoxing.com/createqr?uuid={
# }&xxtrefer=&type=1&mobiletip=JIA%e6%8e%88%e6%9d%83%e8%af%b7%e6%b1%82'.format(str(uuid.uuid4().hex))


headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 ("
                  "@Kalimdor)_11391565702936108810 "
}


def login(conv, user_uuid=0, server=False):
    code_html_url = 'https://passport2.chaoxing.com/cloudscanlogin?mobiletip=JIA%e6%8e%88%e6%9d%83%e8%af%b7%e6%b1%82' \
                    '&pcrefer=http://i.chaoxing.com '
    conv.keep_alive = False
    code_html = conv.get(code_html_url, headers=headers)
    code_html_obj = BeautifulSoup(code_html.content, "lxml")
    login_uuid = code_html_obj.find(id='uuid')['value']
    login_enc = code_html_obj.find(id='enc')['value']
    code_pic_url = code_html_obj.find(id='ewm')['src']
    # print(login_enc)
    # print(login_uuid)
    if not server:
        code_pic = conv.get('https://passport2.chaoxing.com' + code_pic_url, headers=headers)
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
            login_rec_json = conv.post("https://passport2.chaoxing.com/getauthstatus",
                                       {'uuid': login_uuid, 'enc': login_enc}, headers=headers)
            login_rec_dict = json.loads(login_rec_json.content)
            if login_rec_dict['status']:
                # cv2.destroyAllWindows()
                break
            # print("run once")
            # print(login_rec_dict['status'])
            time.sleep(2)
        return conv
    elif server:
        code_pic = conv.get('https://passport2.chaoxing.com' + code_pic_url, headers=headers)
        pic_content = code_pic.content
        pic_base64 = base64.b64encode(pic_content)
        polling_url = r"https://passport2.chaoxing.com/getauthstatus?uuid=" + login_uuid + r"&enc=" + login_enc
        return pic_base64, conv, polling_url


def get_course_list(conv):
    course_list_url_list = []
    course_list_host_url = 'https://mooc1-1.chaoxing.com'
    course_list_url = 'https://mooc1-1.chaoxing.com/visit/courses'

    conv.keep_alive = False

    course_list_html = conv.get(course_list_url, headers=headers)
    html_obj = BeautifulSoup(course_list_html.content.decode('utf-8'), "lxml")
    course_list_all_tag = html_obj.find_all("h3", class_='clearfix')
    for course_one_tag in course_list_all_tag:
        course_one_tag_info = course_one_tag.find("a")
        # print(course_one_tag_info)
        course_one_tag_url = course_list_host_url + course_one_tag_info.attrs['href'].replace(r"&amp;", r"&")
        # print(course_one_tag_url)
        course_one_tag_name = course_one_tag_info.attrs['title']
        couse_one_tag_list = [course_one_tag_name, course_one_tag_url]
        course_list_url_list.append(couse_one_tag_list)
    return course_list_url_list


def get_course_work(conv, course_list):
    host_url = 'https://mooc1-1.chaoxing.com'
    work_list = []
    conv.keep_alive = False
    for course in course_list:
        course_name = course[0]  # 课程名称
        html_content = conv.get(course[1], headers=headers)  # 获取页面内容，response对象
        html_obj = BeautifulSoup(str(html_content.content.decode('utf-8').strip()), 'lxml')  # 解析页面，bs对象
        work_obj = html_obj.find("a", string=r"作业  ")
        work_url = work_obj['data']
        work_url = host_url + work_url

        # TODO：加上直接跳转作业
        # html_content_raw = html_content.content
        # course_id = re.search(r'(?<=classId\s=\s)\d*',html_content_raw)
        # class_id = re.search(r'(?<=courseId\s=\s)\d*',html_content_raw)
        # course_enc = re.search(r'(?<=enc=)\w*',html_content_raw)

        work_info_list = [course_name, work_url]
        work_list.append(work_info_list)

    return work_list
    # worklist = [课程名称,作业url,courseID,classID]


def get_work_info(conv, info_list):
    # cid是课程id

    work_info_obj_list = []

    conv.keep_alive = False

    def is_li_but_has_no_class(tag):
        return tag.name == 'li' and not tag.has_attr('class')

    for work_one_list in info_list:  # 开始处理一门课
        course_name = work_one_list[0]
        html = conv.get(work_one_list[1], headers=headers)  # 请求页面
        html_ul_parse_rule = SoupStrainer("ul", class_="clearfix")
        ul_obj = BeautifulSoup(str(html.content.decode('utf-8').strip()), "lxml",
                               parse_only=html_ul_parse_rule)  # 转换(已经定位到ul)

        undo_work_one_info_list = ul_obj.find_all(is_li_but_has_no_class)

        if undo_work_one_info_list:
            for one in undo_work_one_info_list:
                work_tag_and_name_list = [one, course_name]
                work_info_obj_list.append(work_tag_and_name_list)

    return work_info_obj_list


def parse_work(work_list):
    work_info_list = []

    for one_work in work_list:
        work_info = {}
        work_tag = one_work[0]
        work_course_name = one_work[1]

        work_status = str(work_tag.find('strong').string.strip())

        if work_status == '待做':
            work_name = work_tag.find('a', class_='inspectTask')['title']

            time_list = work_tag.find_all('span', class_='pt5')

            try:
                start_time = time_list[0].contents[1]
            except IndexError:
                start_time = ''
            try:
                end_time = time_list[1].contents[1]
            except IndexError:
                end_time = ''
            # print(start_time)
            # print(end_time)
            # print(work_name)
            # print(work_course_name)
            # print('\n\n')
            work_info['workname'] = work_name
            work_info['coursename'] = work_course_name
            work_info['start'] = start_time
            work_info['end'] = end_time
            work_info_list.append(work_info)

    return work_info_list


# print(html_obj)
# exit(0)
# for one in work_info_obj_list:
#   print(one)
# work_info_list = []
# print(type(tag))
# if tag.name == 'ul' and not tag.has_attr('class'):
# return True
# print(tag.name)
# else:
# return False
# print(ul_obj)
# print("\n\n\n\n")
# print(undo_work_one_info_list)
# print(work_status)
# print(type(work_status))
# print(work_tag)
# print(time_list)
# print(work_tag)
# print('\n\n\n\n')
# print(work_course_name)
# print('\n\n\n\n')
"""
    if work_status == r'待做':
        time_list = work_tag.findall(class_='pt5')
        time_start = time_list[0]
        time_end = time_list[1]
        print(time_start)
        print(time_end)



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
# work_all_obj = html_obj.find("ul",class_="clearfix") # 定位到ul层，独立对象
# work_one_obj_list = html_obj.find_all(is_li_but_has_no_lookLi)  # 找到所有不含有class的ul
# work_one_obj_list = html_obj.find_all('li')
# print(work_one_obj_list)

# if not work_one_obj_list:
# work_url_quote = html_obj.find("a", string=r'作业  ')['data']
# work_url = unquote(work_url_quote)
# work_url = host_url + work_url
# work_url_list.append(work_url)
# print(type(work_url))
# print(work_url)
# work_html = conv.get(work_url,headers=headers)
