#-*-coding:utf8-*-
import re
import requests

#读取源代码文件
f = open('avril_pic.txt','r')
html = f.read()
f.close()


#匹配图片网址
pic_url = re.findall('width="96px" src="(.*?)" alt="',html,re.S)
i = 0
for each in pic_url:
    print 'now downloading:' + each
    hea={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
    pic = requests.get(each,headers=hea)
    fp = open('Avril_pic\\' + str(i) + '.jpg','wb')
    fp.write(pic.content)
    fp.close()
    i += 1