import pymysql

from search.relevancy_introduction import score_introduce
from search.relevency_review import score_review
from search.relevancy_name import score_name

# 导入停用词表
stop = [line.strip() for line in open('./stopwords/stopwords.txt', 'r', encoding='gbk').readlines()]

db = pymysql.connect("localhost", "root", "8520", "coolapk")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def rele(keys):
    wn = 0.5
    wi = 0.4
    wr = 0.1
    # name_value = 0



    introduce = score_introduce(keys)
    # print(introduce)
    review = score_review(keys)
    name = score_name(keys)
    score = {}
    for i in review:
        # print(i)
        score[i] = 0
    for i in introduce:
        score[i] = 0
    for i in name:
        score[i] = 0
    # print('@@@@@@@@@@@@@@@@@',score)

    for index in score:
        # print(index)
        ind = 0
        nam = 0
        rev = 0
        a = 1
        b = 1
        c = 1
        # print(introduce[index])
        try:
            ind = introduce[index]
        except:
            ind = 0
        try:
            rev = review[index]
        except:
            rev = 0
        try:
            nam = name[index]
        except:
            nam = 0
        if ind == 0:
            a = 0
        if rev == 0:
            b = 0
        if nam == 0:
            c = 0
        # print(ind,rev,nam)
        try:
            score[index] = (wn * nam + wr * rev + wi * ind) / (a * wi + b * wr + wn * c)
        except:
            score[index] = 0

    try:
        # 执行sql语句
        sql = """select * from download_apk where name = '{}'""".format(keys)
        cursor.execute(sql)
        result = cursor.fetchall()

        # print(result)
        # 提交到数据库执行
        db.commit()
        score[result[0][3]] += 100
        # print(result)
    except:
        print("找不到这个app")
        # print(words[0], word)
        # db.close()
        # 如果发生错误则回滚
        # exit(0)
    # print(introduce)
    # print(score)
    return sorted(score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)


if __name__ == "__main__":
    keys = rele("短视频")
    print(keys)
    # print(sorted(keys.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    # print(keys['/apk/com.tencent.mm'])
    # for key in keys:
    #     print(key,keys[key])
    #     # break
    # print(keys)
