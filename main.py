import requests,json

from func import *

conv = requests.session()

conv_login = login(conv) # 登录

print("登录成功")

backclazzdata(conv_login) # 抓取课程列表




"""
if __name__ == '__main__':
    pass
"""