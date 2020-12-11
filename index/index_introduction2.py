import jieba
import pymysql
import re

# 导入停用词表
stop = [line.strip() for line in open('../stopwords/stopwords.txt', 'r', encoding='gbk').readlines()]

# insert_w = []
# connect MySQL
db = pymysql.connect("localhost", "root", "8520", "coolapk")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def create_index_introduction(introduction):
    skip_url = introduction[0]
    coolapk_introduction = introduction[1]
    seg_list = jieba.cut_for_search(coolapk_introduction, HMM=False)
    seg_list_dic = []
    for seg in seg_list:
        if seg not in stop:
            seg_list_dic.append(seg)
    # print(skip_url, ", ".join(seg_list_dic))

    return skip_url, seg_list_dic


def insert_words(words):
    for word in words[1]:
        word = word.strip()
        if (word != '') & (word != '\\'):
            try:
                # 执行sql语句
                sql = """select * from index_introduction where words = '{}'""".format(word)
                cursor.execute(sql)
                num_word = cursor.fetchall()
                # 提交到数据库执行
                db.commit()
            except:
                print("error")
                print(words[0],word)
                # db.close()
                # 如果发生错误则回滚
                # exit(0)
            # print(num_word)
            try:
                skip_url = num_word[0][1]
                if skip_url is None:
                    skip_url = words[0]
                else:
                    skip_url = skip_url + ' ' + words[0]
                try:
                    sql = """update index_introduction set skip_urls = '{}' where words = '{}'""".format(skip_url, word)
                    cursor.execute(sql)
                    db.commit()
                except:
                    print("update error")
                    print(words[0], word)
                    # db.close()
                    # 如果发生错误则回滚
                    # exit(0)
            except:
                print("update error")
                print(words[0], word)
                # db.close()
                # 如果发生错误则回滚
                # exit(0)


if __name__ == "__main__":

    try:
        sql = """select skip_url,introduction from download_apk"""
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()

    except:
        print("读取数据skip_url,introduction失败")
        db.rollback()
        exit(0)
    # 分词

    y = 0
    for item in result:
        if item[1] != '0':
            temp = item[1].split("@")
            # print(temp)
            str_temp = temp[0]
            item = (item[0], str_temp)
            # print(item[1])
            words = create_index_introduction(item)
            # print(words)
            insert_words(words)
        y += 1
        if y % 50 == 0:
            print("目前文章数：",y)
    print("第二次遍历分词结束")

    db.close()
