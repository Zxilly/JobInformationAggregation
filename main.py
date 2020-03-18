import requests

import func
import mobile_func

conv = requests.session()

conv_login = func.login(conv=conv)  # 登录

course_list = mobile_func.get_course(conv_login)

print(mobile_func.get_work(conv_login,course_list))

#print("登录成功")

#course_list = get_course_list(conv_login)  # 获取课程对应url
# 返回一个含有所有课程名称和url的列表

#print(course_list)


#course_work_list = get_course_work(conv_login, course_list)
# 返回一个含有所有课程名称和作业url的列表

#all_work_info_tag_list = get_work_info(conv_login,course_work_list)
# 返回一个含有所有待做作业tag的列表

#all_work_info_dict_list = parse_work(all_work_info_tag_list)
# 返回一个含有所有待做作业信息的列表

#print(all_work_info_dict_list)


#work_info_list = get_work_info(conv_login, course_list)




# course_info_dict = backclazzdata(conv_login) # 抓取课程列表

# gettask(course_info_dict,conv_login)
