import urllib.request
from bs4 import BeautifulSoup
import pymysql
import re
import requests

def spider(url):
    # connect MySQL
    db = pymysql.connect("localhost", "root", "8520", "coolapk")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    img_url = ''
    download_url = ''
    skip_url = ''
    name = ''
    version = ''
    download_count = ''
    focus_count = ''
    comment_count = ''
    language = ''
    coolapk_review = ''
    new_features = ''
    introduction = ''
    score = 0.0
    category_labels = ''
    detailed_information = ''
    permissions = ''
    skip_url = url
    url = 'https://www.coolapk.com' + url
    html = requests.get(url, timeout=60).text
    soup = BeautifulSoup(html, 'html.parser')

    ######
    # 爬取apk_topbar区域
    list_apk_topbar = soup.find_all('div', class_='apk_topbar')
    apk_topbar = list_apk_topbar[0]
    # 爬取apk图标和下载二维码
    list_apk_topbar_img = apk_topbar.find_all('img')
    img_url = str(list_apk_topbar_img[0]).replace('amp;', '').replace('<img src="', '').replace('"/>', '')
    # print(img_url)

    download_url = 'https://www.coolapk.com' + str(list_apk_topbar_img[1]).replace('amp;', '').replace('<img src="',
                                                                                                       '').replace(
        '"/>', '')
    # print(download_url)
    # for item in list_apk_topbar_img:
    #     print(str(item).replace('amp;', '').replace('<img src="', '').replace('"/>', ''))
    #     print('************************************************************************')
    ###############
    # 爬取apk名字、版本号
    list_apk_topbar_detail_app_title = apk_topbar.find_all('p', class_='detail_app_title')
    text = None
    for item in list_apk_topbar_detail_app_title:
        text = re.split(r'  ', str(item.text))
        # print(text)
    name = text[0]
    version = text[1]
    # print(name,version)

    # 爬取下载数目、关注数、评论数、语言等信息
    list_apk_topbar_apk_topba_message = apk_topbar.find_all('p', class_='apk_topba_message')
    for item in list_apk_topbar_apk_topba_message:
        text = re.split(r'[\s]', str(item.text))
        while True:
            try:
                text.remove('')
            except:
                break
        while True:
            try:
                text.remove('/')
            except:
                break
        # print(text)
    download_count = text[1]
    focus_count = text[2]
    comment_count = text[3]
    language = text[4]
    # print(download_count,focus_count,comment_count,language)
    #####################
    # 爬取酷安点评
    list_apk_left_first_title = soup.find_all('div', class_='apk_left_first-title')
    # for item in list_apk_left_first_title:
    #     print(item)
    apk_left_first_title = list_apk_left_first_title[0]

    apk_left_title_nav1 = apk_left_first_title.find_all('p', class_='apk_left_title_nav')
    coolapk_review = False
    if apk_left_title_nav1[0].text == '酷安点评':
        coolapk_review = True
        apk_left_title_info1 = apk_left_first_title.find_all('p', class_='apk_left_title_info')
        text = re.split(r'[\s]', apk_left_title_info1[0].text)
        while True:
            try:
                text.remove('')
            except:
                break
        while True:
            try:
                text.remove('/')
            except:
                break
        coolapk_review = ''
        for item in text:
            coolapk_review += str(item) + ' '
        # print(coolapk_review)
        # print('###############################')

    #########################
    ##
    list_apk_left_title = soup.find_all('div', class_='apk_left_title')
    for item in list_apk_left_title:
        apk_left_title_nav = item.find_all('p', class_='apk_left_title_nav')
        # print(apk_left_title_nav[0].text)
        if apk_left_title_nav[0].text == '新版特性':
            apk_left_title_info = item.find_all('p', class_='apk_left_title_info')
            # print(apk_left_title_info[0].text.strip())
            new_features = apk_left_title_info[0].text.strip()
            # print(new_features)
        elif apk_left_title_nav[0].text == '应用简介':
            apk_left_title_info = item.find_all('div', class_='apk_left_title_info')
            # print(apk_left_title_info[0].text.strip())
            introduction = apk_left_title_info[0].text.strip()
            # print(introduction)
        elif apk_left_title_nav[0].text == '应用评分':
            rank_num = item.find_all('p', class_='rank_num')
            # print(float(rank_num[0].text))
            score = float(rank_num[0].text)
            # print(score)
        elif apk_left_title_nav[0].text == '分类标签':
            apk_left_span2 = item.find_all('span', class_='apk_left_span2')
            # print(apk_left_span2)
            category_labels = ''
            for i in range(len(apk_left_span2)):
                category_labels += str(apk_left_span2[i].text) + ' '
            # print(category_labels)
        elif apk_left_title_nav[0].text == '详细信息':
            apk_left_title_info = item.find_all('p', class_='apk_left_title_info')
            # print(apk_left_title_info[0].text.strip().replace(' ', ''))
            detailed_information = apk_left_title_info[0].text.strip().replace(' ', '')
            # print(detailed_information)
        elif apk_left_title_nav[0].text == '权限信息':
            apk_left_title_info = item.find_all('div', class_='apk_left_title_info')
            # print(apk_left_title_info[0].text.strip().replace(' ', ''))
            permissions = apk_left_title_info[0].text.strip().replace(' ', '')
            # print(permissions)

    #######
    # 将爬取的信息存入数据库
    cursor.execute("""INSERT INTO download_apk(img_url,download_url,skip_url,name,version,download_count,\
                                                focus_count,comment_count,language,coolapk_review,new_features,introduction,\
                                                score,category_labels,detailed_information,permissions) VALUES(%s,%s,%s,%s,%s,%s,\
                                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (img_url, download_url, skip_url,
                                                                                    name, version, download_count, \
                                                                                    focus_count, comment_count,
                                                                                    language, coolapk_review,
                                                                                    new_features, introduction, \
                                                                                    score, category_labels,
                                                                                    detailed_information, permissions))
    db.commit()
    db.close()



if __name__ == "__main__":
    db = pymysql.connect("localhost", "root", "8520", "coolapk")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    ## 删除数据库
    try:
        sql = """drop table download_apk"""
        cursor.execute(sql)
        db.commit()
    except:
        print("can't find db download_apk")
    ##
    ##
    ##
    ##
    # 创建数据库
    try:
        sql = """Create table download_apk(
                  id int not null AUTO_INCREMENT,\
                  img_url longtext not null,\
                  download_url longtext not null, \
                  skip_url longtext not null,\
                  name longtext not null,\
                  version longtext,\
                  download_count longtext,\
                  focus_count longtext,\
                  comment_count longtext ,\
                  language longtext,\
                  coolapk_review longtext,\
                  new_features longtext,\
                  introduction longtext,\
                  score numeric(5,1),\
                  category_labels longtext,\
                  detailed_information longtext,\
                  permissions longtext,\
                  CONSTRAINT url_id PRIMARY KEY (id)
                  )"""
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("create db error")
    sql = "select * from urllist"
    cursor.execute(sql)
    result = cursor.fetchall()
    db.commit()
    db.close()
    i = 0
    for item in result:

        try:
            spider(item[0])
            i += 1
            print(i,item[0])
        except:
            print("error",item[0])
    print('爬取完成')
