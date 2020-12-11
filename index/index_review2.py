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


def create_index_review(review):
    skip_url = review[0]
    coolapk_review = review[1]
    seg_list = jieba.cut_for_search(coolapk_review, HMM=False)
    seg_list_dic = []
    for seg in seg_list:
        if seg not in stop:
            seg_list_dic.append(seg)
    # print(skip_url, ", ".join(seg_list_dic))

    return skip_url, seg_list_dic
    # seg_list = jieba.cut_for_search("1.可以发语音、文字消息、表情、图片、视频30M流量可以收发上千条语音，省电省流量\
    # 2.朋友圈，跟朋友们分享生活点滴\
    # 3.摇一摇、查看附近的人，世界不再有陌生人\
    # 4.扫一扫，可以扫商品条码、图书封面、CD封面，甚至扫描英文单词来翻译成中文\
    # 5.公众帐号，用微信关注明星、看新闻、设提醒\
    # 6.游戏中心，和朋友们一起玩游戏\
    # 7.表情商店，有趣好玩的表情在这里特别说明：微信只消耗网络流量，不产生短信电话费用", HMM=False)  # 搜索引擎模式
    # seg_list_dic = []
    # for seg in seg_list:
    #     if seg not in stop:
    #         seg_list_dic.append(seg)
    # print(", ".join(seg_list_dic))
    #
    # # jieba.cut的默认参数只有三个,jieba源码如下
    # # cut(self, sentence, cut_all=False, HMM=True)
    # # 分别为:输入文本 是否为全模式分词 与是否开启HMM进行中文分词


def insert_words(words):
    for word in words[1]:
        word = word.strip()
        if word != '':
            try:
                # 执行sql语句
                sql = """select * from index_review where words = '{}'""".format(word)
                cursor.execute(sql)
                num_word = cursor.fetchall()
                # 提交到数据库执行
                db.commit()
            except:
                print("error")
                # db.close()
                # 如果发生错误则回滚
                exit(0)
            # print(num_word)
            skip_url = num_word[0][1]
            if skip_url is None:
                skip_url = words[0]
            else:
                skip_url = skip_url + ' ' + words[0]
            try:
                sql = """update index_review set skip_urls = '{}' where words = '{}'""".format(skip_url, word)
                cursor.execute(sql)
                db.commit()
            except:
                print("update error")
                # db.close()
                # 如果发生错误则回滚
                exit(0)


if __name__ == "__main__":

    try:
        sql = """select skip_url,coolapk_review from download_apk"""
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()

    except:
        print("读取数据skip_url,coolapk_review失败")
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
            words = create_index_review(item)
            # print(words)
            insert_words(words)
        y += 1
        if y % 500 == 0:
            print("目前文章数：",y)
    print("第二次遍历分词结束")

    db.close()
