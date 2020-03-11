import requests

from func import *

headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 (@Kalimdor)_11391565702936108810"
}

conv = requests.session()

conv_login = login(conv)

test_html = conv_login.get('http://mooc1-1.chaoxing.com/work/getAllWork?classId=15512590&courseId=207720284&isdisplaytable=2&mooc=1&ut=s&enc=2797af767c1f2bd033888bc4ed26b020&cpi=92764071&openc=2daa25c368ec65fdf5c790def1587c12',headers=headers)
print(test_html.content.decode('utf-8'))