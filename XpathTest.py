#-*-coding:utf8-*-
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def towrite(contentdict):
    f.writelines(u'标题：' + str(contentdict['title'] + '\n'))



def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//table[@class="list-table"]')
    item = {}
    for each in content_field:
        title = each.xpath('@title/text()')
        print title
        item['title'] = title
        towrite(item)


if __name__=='__main__':
    pool = ThreadPool(4)
    f = open('content.txt','a')
    page = []
    for i in range(1,5):
        newpage = 'http://nz.gdcct.net/market/supplyList.jspx?currIndex='+str(i)+'&fCode=008&cssId=supply&category=3'
        page.append(newpage)
        
    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()