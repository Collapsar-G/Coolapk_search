import jieba
import pymysql
import re

# 导入停用词表
stop = [line.strip() for line in open('../stopwords/stopwords.txt', 'r', encoding='gbk').readlines()]

# insert_w = []


def create_index_name(name):
    skip_url = name[0]
    coolapk_name = name[1]
    seg_list = jieba.cut_for_search(coolapk_name, HMM=False)
    seg_list_dic = []
    for seg in seg_list:
        if seg not in stop:
            seg_list_dic.append(seg)
    # print(skip_url, ", ".join(seg_list_dic))

    return skip_url, seg_list_dic

def insert_words(words):
    db = pymysql.connect("localhost", "root", "8520", "coolapk")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    for word in words[1]:
        word = word.strip()
        if word != '':
            try:
                # 执行sql语句
                cursor.execute("""INSERT INTO index_name(words) VALUES(%s)""", (word))
                # 提交到数据库执行
                db.commit()
            except:
                # print("error")
                # 如果发生错误则回滚
                db.rollback()


if __name__ == "__main__":
    # connect MySQL
    db = pymysql.connect("localhost", "root", "8520", "coolapk")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # sql = "drop table index_name"
    # cursor.execute(sql)

    # try:
    #     sql = """Create table index_name(
    #                     words_id int not null AUTO_INCREMENT,\
    #                     words varchar(20)  not null,\
    #                     skip_urls longtext ,\
    #                     num int,\
    #                     primary key (words)
    #                     )"""
    #     cursor.execute(sql)
    # except:
    #     print("创建index_name表失败")
    #     db.rollback()
        # exit(0)
    sql = """Create table index_name( 
                            words varchar(20)  not null,\
                            skip_urls longtext ,\
                            primary key (words)
                            )"""
    cursor.execute(sql)
    # 从download_apk中读取name
    try:
        sql = """select skip_url,name from download_apk"""
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()

    except:
        print("读取数据skip_url,coolapk_name失败")
        db.rollback()
        exit(0)
    # 分词
    db.close()
    y = 0
    for item in result:
        if item[1] != '0':
            temp = item[1].split("@")
            # print(temp)
            str_temp = temp[0]
            item = (item[0], str_temp)
            # print(item[1])
            words = create_index_name(item)
            # print(words)
            insert_words(words)
            # insert_words(words)
        # print("!!!!!!!!!!!!!!!!!", y)
        y += 1
        if y % 500 == 0:
            print("目前文章数：",y)
    print("第一次遍历分词结束")
    # f = open(r'index_name.txt', 'a')
    #
    # f.write('\n'.join(insert_w))
    #
    # f.close()
