#-*-coding:utf8-*-
import requests
import re

hea={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
html = requests.get('http://nz.gdcct.net/market/supplyList.jspx?fCode=008',headers = hea)
html.encoding = 'utf-8'
# print html.text
title = re.findall('target="_blank" title="(.*?)">', html.text, re.S)
for each in title:
    print each