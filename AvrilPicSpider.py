#-*-coding:utf8-*-
import re
import requests

#读取源代码文件
f = open('avril_pic.txt','r')
html = f.read()
f.close()

#匹配图片网址
pic_url = re.findall('<img class="main_img img-hover" src="(.*?)" style',html,re.S)
i = 0
for each in pic_url:
    print 'now downloading:' + each
    pic = requests.get(each)
    fp = open('Avril_pic\\' + str(i) + '.jpg','wb')
    fp.write(pic.content)
    fp.close()
    i += 1