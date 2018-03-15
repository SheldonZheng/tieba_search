#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
import json
import sys
def trim(s):
    if s[:1] != ' ' and s[-1:] != ' ':
        return s
    elif s[:1] == ' ':
        return trim(s[1:])
    else:
        return trim(s[:-1])

continue_ = True
page_id = sys.argv[1]
pageNo = 1
filter_str = sys.argv[2]
base_jump_url = 'http://c.tieba.baidu.com/p/%s?pid=%s&cid=0#%s'

while continue_:
    continue_ = False
    url = 'https://tieba.baidu.com/p/%s?pn=%s' % (page_id,pageNo)
    print(url)
    print('pageNo:' ,pageNo)
    #print(url)
    r = requests.get(url=url)
    data = r.text
    soup = BeautifulSoup(data, 'html5lib')
    pageData = soup.find_all(class_=re.compile('l_pager pager_theme_4 pb_list_pager'))
    #print(pageData[0].text)
    #print('下一页' in pageData[0].text)
    if '下一页' in pageData[0].text:
        continue_ = True
        pageNo += 1
#class_result = soup.find_all(attrs={'class':'l_post l_post_bright j_l_post clearfix'})
#class_result = soup.find_all(class_='l_post l_post_bright j_l_post clearfix  ')
    class_result = soup.find_all(class_=re.compile('l_post l_post_bright j_l_post clearfix*'))
    for str in class_result:
    #print(str)
        data_field_str = str['data-field']
    #print(data_field_str)
        json_data_field = json.loads(data_field_str)
        post_id = json_data_field['content']['post_id']
    #print(post_id)
        text = str.find(class_=re.compile('d_post_content j_d_post_content')).text
        if filter_str in text :
            print(trim(text),'\t',base_jump_url % (page_id,post_id,post_id))
        #f.write(trim(text),'\t',base_jump_url % (page_id,post_id,post_id))
        #print('next**********************************\n')
