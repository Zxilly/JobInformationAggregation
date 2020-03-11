import requests

from func import *

conv = requests.session()

conv_login = login(conv)  # 登录

print("登录成功")

course_url_list = get_course_list(conv_login)  # 获取课程对应url
# 返回一个含有所有课程url的列表

course_work_list = get_course_work(conv_login, course_url_list)
# 返回一个含有所有作业url的列表

work_info_list = get_work_info(conv_login, course_url_list)
# 返回一个含有所有待做作业信息的列表



# course_info_dict = backclazzdata(conv_login) # 抓取课程列表

# gettask(course_info_dict,conv_login)
