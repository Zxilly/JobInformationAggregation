with open('a.dat','w+') as f:
    f.write('aaa')


"""
from bs4 import  BeautifulSoup
import lxml
html_doc = '<head></head><span class="pt5" title=""><span class="fl">开始时间：</span></span>'

html2_doc = ['<span class="pt5" title=""><span class="fl">开始时间：</span>2020-03-10 14:02</span>'
            '<span class="pt5" title=""><span class="fl">截止时间：</span>2020-03-10 14:02</span>']


soup = BeautifulSoup(html_doc,"lxml")

test1 = soup.span
test = test1.contents[1]

print(test)
#print(soup.find_all(has_class_but_no_id))

# string_test = "                                  aaa                                      "
# print(string_test.strip())
"""
