#-*-coding:utf8-*-
import requests
import DBUtil
import uuid
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print'开始爬取内容啦。。。。。。'
        
#changepage方法用来产生不同页数：
    def changepage(self,url,total_page): 
        now_page = int(re.search('currIndex=(\d+)',url,re.S).group(1))  
        page_group = [] 
        for i in range(now_page,total_page+1):
            link = re.sub('currIndex=\d+', 'currIndex=%s'%i, url, re.S)
            page_group.append(link)
        return page_group  
#getsource用来获取网页源代码：
    def getsource(self,url): 
        html = requests.get(url) 
        return html.text
#geteveryclass用于抓取每个新闻列表的信息
    def geteveryclass(self,source):
        everyclass = re.findall('list-table">(.*?)</table>', source, re.S)
        return everyclass

#getlist用于从每个列表提取需要的信息
    def getlist(self,eachclass):
        list = re.findall('target="_blank">(.*?)</tr>', eachclass, re.S)
        return list
#getinfo用于将列表中的信息分类
    def getinfo(self,eachlist):
        info = {}
        info['title'] = re.search('title="(.*?)">',eachlist,re.S).group(1)
        info['description'] = re.search('description">(.*?)</p>', eachlist, re.S).group(1)
        info['date']=re.search('p2date">(.*?)</p>',eachlist,re.S).group(1)
        info['address'] = re.search('class="p4 p2date">(.*?)</p>', eachlist, re.S).group(1)            
        return info
#saveinfo用来保存结果到info.txt文件中
    def saveinfo(self,classinfo):
        f = open('info.txt','a')
        for each in classinfo:
            sql = 'insert into news_info(Id,title,description,date,address) values(%s,%s,%s,%s,%s)'
            util = DBUtil.DBUtilTest()
            util.insert(sql,[uuid.uuid1(),each['title'],each['description'].strip(),each['date'],each['address']])
#             util.insert(sql, [uuid.uuid1(),'你好夏天','hehe','2015-7-15','hh'])
            print'已成功保存至mysql'
            
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('description:' + each['description'].strip()+'\n')
            f.writelines('date:' + each['date'] + '\n')
            f.writelines('address:' + each['address'] + '\n\n')
        f.close()

if __name__ == '__main__':
    classinfo = []
    url = 'http://nz.gdcct.net/market/supplyList.jspx?currIndex=1&fCode=008&cssId=supply&category=3'
    newsSpider = spider()
    all_links = newsSpider.changepage(url,3)
    for link in all_links:
        print'正在处理页面：'+link
        html = newsSpider.getsource(link)
        everyclass = newsSpider.geteveryclass(html)
#         print everyclass[0]
        for each in everyclass:
            list = newsSpider.getlist(each)
#             print list
            for er in list:
#                 print er
                info = newsSpider.getinfo(er)
                
#                 print info
                classinfo.append(info)
#                 print classinfo[0]
    newsSpider.saveinfo(classinfo)
