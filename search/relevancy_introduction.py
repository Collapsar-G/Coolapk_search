import jieba
import numpy as np
import pymysql
import re

# 导入停用词表
stop = [line.strip() for line in open('./stopwords/stopwords.txt', 'r', encoding='gbk').readlines()]

db = pymysql.connect("localhost", "root", "8520", "coolapk")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def search_index(key):
    # seg_list = jieba.cut_for_search(key, HMM=False)
    seg_list = jieba.lcut(key, HMM=False)
    # print(seg_list)
    seg_list_dic = []
    for seg in seg_list:
        seg = seg.strip()
        if (seg != '') & (seg != '\\'):
            if seg not in stop:
                seg_list_dic.append(seg)

    num = {}
    for seg in seg_list_dic:
        try:
            # 执行sql语句
            sql = """select * from index_introduction where words = '{}'""".format(seg)
            cursor.execute(sql)
            result = cursor.fetchall()
            # print(result)
            num[seg] = result[0][1]
            # 提交到数据库执行
            db.commit()
        except:
            print("error")
            # print(words[0], word)
            # db.close()
            # 如果发生错误则回滚
            # exit(0)
    # print(num)
    return num


def count(words):
    for seg in words:

        words[seg] = words[seg].split(' ')
        # print(words[seg])
        l = []
        h = {}
        for index in words[seg]:
            if index in l:
                h[index] = 1 + h[index]
            else:
                h[index] = 1
        words[seg] = h
        # print(".............................", seg, words[seg])
    return words


def score(count):
    w = {}

    for word in count:
        for index in count[word]:
            count[word][index] = count[word][index] * np.log(2344 / len(count[word]))
            # print("@@@@@@@@@@",count[word][index])
        # print(word, count[word])
        # print()
    # print(count)
    return count


def relevancy(scor):
    score_artical = {}
    for word in scor:
        for index in scor[word]:
            s = 0
            try:
                s = score_artical[index]
            except:
                # print('error')
                s = 0
            score_artical[index] = s + scor[word][index]
            # print(index,score_artical[index])
    # for i in sorted(score_artical.items(), key=lambda kv: (kv[1], kv[1]),reverse=True):
    #     print(i)
    # return sorted(score_artical.items(), key=lambda kv: (kv[1], kv[1]), reverse=True)
    return score_artical

def score_introduce(search_key):
    keys = search_index(search_key)
    # print(keys)
    cou = count(keys)
    scor = score(cou)
    re = relevancy(scor)
    return re


if __name__ == "__main__":
    keys = score_introduce("短视频")
    print(keys)
#
