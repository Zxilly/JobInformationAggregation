import json
from urllib.parse import unquote
from bs4 import BeautifulSoup, SoupStrainer

# https://mobilelearn.chaoxing.com/task/getStuWorkAndExamSkipUrl?courseId=207435085&classId=15512774

headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 ("
                  "@Kalimdor)_11391565702936108810 "
}

parser_ul = SoupStrainer('ul')


def get_course(conv):
    url = 'https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&mcode='
    course_info_dict_list = []
    course_list_obj = conv.get(url, headers=headers)
    course_list_dict = json.loads(course_list_obj.content)
    for one in course_list_dict['channelList']:
        course_info_dict = {}
        course_info_dict['course_id'] = one['content']['course']['data'][0]['id']
        #try:
        #    course_info_dict['image_url'] = one['content']['course']['data'][0]['imageurl']
        #except KeyError:
        #    course_info_dict['image_url'] = None
        course_info_dict['course_name'] = one['content']['course']['data'][0]['name']
        course_info_dict['class_id'] = one['key']
        course_info_dict_list.append(course_info_dict)
    # print(course_info_dict_list)
    return course_info_dict_list


def get_work(conv, course_info):
    work_info = []
    url = 'https://mobilelearn.chaoxing.com/task/getStuWorkAndExamSkipUrl'
    for one_course in course_info:
        # print(one)
        html_obj = conv.get(url, headers=headers,
                            params={'courseId': one_course['course_id'], 'classId': one_course['class_id']})
        html_bs = BeautifulSoup(str(html_obj.content.decode('utf-8')), 'lxml', parse_only=parser_ul)
        #print(html_bs.prettify())
        work_list = html_bs.find_all('li')
        for one_task in work_list:
            if (one_task.find('span').string == '未交'):
                #print(one_task)
                work_name = str(one_task.find('p').string)
                try:
                    left_time = str(one_task.find('span',class_='fr').string)
                except AttributeError:
                    left_time = '不限时'
                course_name = str(one_course['course_name'])
                work_url = unquote(str(one_task['data']))
                work_info.append({'work_name':work_name,'course_name':course_name,'left_time':left_time,'work_url':work_url})
            # print(str(one_task.find('p').string))
    return work_info

