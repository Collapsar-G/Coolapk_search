import urllib.request
from bs4 import BeautifulSoup
import pymysql
import re

# connnect MySQL
db = pymysql.connect("localhost", "root", "8520", "coolapk")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# sql = """Create table urllist(
#         url char(100) not null)"""
# cursor.execute(sql)

for i in range(1, 290):
    # specify the url
    quote_page = 'https://www.coolapk.com/apk?p=' + str(i)
    # query the website and return the html to the variable 'page'
    request = urllib.request.Request(quote_page)
    page = urllib.request.urlopen(request)

    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # get the url and name of each apk
    name_box = soup.find_all('a')
    for link in name_box:
        if (re.findall('\/apk\/com\..*', link.get('href'))):
            href = link.get('href')
            # print(type(href))
            try:
                # 执行sql语句

                cursor.execute("""INSERT INTO urllist(url) VALUES(%s)""", (href))
                # 提交到数据库执行
                db.commit()
            except:
                print("error")
                # 如果发生错误则回滚
                db.rollback()
    print("page %d end", i)
# 关闭数据库连接
sql =  "delete FROM urllist WHERE url LIKE '%%{}%%'".format('?')
print(sql)
cursor.execute(sql)
db.commit()
db.close()
