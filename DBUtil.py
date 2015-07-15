#-*-coding:utf8-*-
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DBUtilTest:
    
    def insert(self,sql,values):

        conn = MySQLdb.connect(host = 'localhost', port = 3306, user = 'root',passwd = '123456', db = 'test_hongye',charset='utf8')

        cur = conn.cursor()

        cur.execute(sql,values)
        
        cur.close()

        conn.commit()

        conn.close()       
        
        
if __name__ == '__main__':
    util = DBUtilTest();
#     sql = 'insert into news_info values(%s,%s,%s,%s,%s)'
#     util.insert(sql,['2','求购','描述','2015-7-15','合肥市'])
#     print '连接数据库成功'