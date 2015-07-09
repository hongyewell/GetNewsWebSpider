#-*-coding:utf8-*-
import requests
import re

i=0
while i <2:
    url = 'http://nz.gdcct.net/market/supplyList.jspx?currIndex='+str(i)+'&fCode=008&cssId=supply&category=3'
    html = requests.get(url).text
    title = re.findall('target="_blank" title="(.*?)">', html, re.S)
    for each in title:
       print each
i+=1