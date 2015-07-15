# -*- coding: utf-8 -*-
'''
Created on 2015年4月16日
@author: miying
'''
import urllib2
import re
import uuid
import chardet
from bs4 import BeautifulSoup
import DBUtil

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 发送请求
def getHtml(url):
    try:
        req = urllib2.Request(url)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'
        req.add_header('User-Agent', user_agent)
        
        resp = urllib2.urlopen(req)
        html_1 = resp.read()
        
        # 获取html_1的编码方式
        mychar = chardet.detect(html_1)
        html_encode = mychar['encoding']
        
        if html_encode == 'utf-8' or html_encode == 'UTF-8':
            html = html_1
        else :
            html = html_1.decode('gb2312','ignore').encode('utf-8')
            
        
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print e.code
        if hasattr(e, 'reason'):
            print e.reason
        
    return html    

def parserLinks(links):
    for link in links:
        for l in link:
            getContent(l)

                       
# 根据链接爬取文章的标题和摘要等信息
def getContent(l):
    url = 'http://www.xinnong.com'
    url += l
    html = getHtml(url)

    pattern = re.compile('<div.*?class="arctit">.*?<h1>(.*?)</h1>.*?<div.*?class="arcinfo">发布时间：(.*?)&nbsp;&nbsp;(.*?)</div>'
                         + '.*?<div.*?class="arcdes">(.*?)</div>.*?</div>.*?<div.*?class="arcont" id="article">(.*?)</div>', re.S)
    items = pattern.findall(html)

    print 'start...'
    
    for item in items:
        
        sql = 'insert into t_articles(objectId, title, publishDate, summary, content) values(%s, %s, %s, %s, %s)'
        DBUtil.DBUtil().insert(sql, (uuid.uuid1(), item[0], item[1].replace('-', ''), item[3], item[4]))

    #    print "url =", url, "title =", item[0], "date =", item[1].replace('-', ''), "from =", item[2], "summary =", item[3], "content = ", item[4]
    
    print 'finished!'        

# 获得总页数
def getTotalPage(url):
    html = getHtml(url)

    pattern = re.compile('<span.*?class="pageinfo">.*?<strong>(.*?)<strong>.*?</span>')
    totals= pattern.findall(html)
#    print totals
    for t in totals:
        return t[0] # 总页数

        
# 获取文章链接分页列表
def getLinks(url, startPage, endPage):
    my_links = []
    for i in range(startPage, endPage):

        # 存储加工
        my_url = url
        my_url += '/p' + str(i) + '.shtml'

        print my_url
        
        # 获得html
        html = getHtml(my_url)

        soup = BeautifulSoup(html)
        html = soup.find_all('div', class_='newslist')
        
        for link in html:
            linkPattern = re.compile("href=\"(.+?)\"")
            links = linkPattern.findall(str(html));
            print links
            my_links.append(links)

        '''
        newslist_index = html.find('newslist')
        lstpage_index = html.find('lstpage', newslist_index)

        html = html[newslist_index - 12 : lstpage_index - 18]
        '''

        '''
        linkPattern = re.compile("href=\"(.+?)\"")
        links = linkPattern.findall(html);
        
        my_links.append(links)
        '''

    return my_links

# 小麦品种： http://www.xinnong.com/xiaomai/xiaomaipinzhong/
# 麦种处理：http://www.xinnong.com/xiaomai/maizhongchuli/
# 种植技术：http://www.xinnong.com/xiaomai/zhongzhijishu/
# 高产种植：http://www.xinnong.com/xiaomai/gaochanzhongzhi/
# 春麦种植：http://www.xinnong.com/xiaomai/chunmaizhongzhi/
# 冬麦种植：http://www.xinnong.com/xiaomai/dongmaizhongzhi/
# 肥水管理：http://www.xinnong.com/xiaomai/feishuiguanli/
# 麦病防治：http://www.xinnong.com/xiaomai/maibingfangzhi/
# 麦虫防治：http://www.xinnong.com/xiaomai/maichongfangzhi/
# 麦田除草：http://www.xinnong.com/xiaomai/maitianchucao/
# 生态种植：http://www.xinnong.com/xiaomai/shengtaizhongzhi/
# 存储加工：http://www.xinnong.com/xiaomai/chucangjiagong/

if __name__ == '__main__':
    # 种类列表
    category = ['/xiaomaipinzhong', '/maizhongchuli', '/zhongzhijishu', '/gaochanzhongzhi',
            '/chunmaizhongzhi', '/dongmaizhongzhi', '/feishuiguanli', '/maibingfangzhi',
             '/maichongfangzhi', '/maitianchucao', '/shengtaizhongzhi', '/chucangjiagong']

#   my_links = getLinks(1, 2)
#   parserLinks(my_links)

#   test
    for x in category:
        print 'http://www.xinnong.com/xiaomai' + x
        url = 'http://www.xinnong.com/xiaomai' + x
        total_page = getTotalPage(url)

        print 'total_page = ', total_page

        my_links = getLinks(url, 1, int(total_page)+1)
        parserLinks(my_links)
    
