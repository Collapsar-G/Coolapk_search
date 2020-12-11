import jieba
import pymysql
import re

# 导入停用词表
stop = [line.strip() for line in open('../stopwords/stopwords.txt', 'r', encoding='gbk').readlines()]

# insert_w = []


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
    db = pymysql.connect("localhost", "root", "8520", "coolapk")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    for word in words[1]:
        word = word.strip()
        if word != '':
            try:
                # 执行sql语句
                cursor.execute("""INSERT INTO index_review(words) VALUES(%s)""", (word))
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
    sql = "drop table index_review"
    cursor.execute(sql)

    # try:
    #     sql = """Create table index_review(
    #                     words_id int not null AUTO_INCREMENT,\
    #                     words varchar(20)  not null,\
    #                     skip_urls longtext ,\
    #                     num int,\
    #                     primary key (words)
    #                     )"""
    #     cursor.execute(sql)
    # except:
    #     print("创建index_review表失败")
    #     db.rollback()
        # exit(0)
    sql = """Create table index_review( 
                            words varchar(20)  not null,\
                            skip_urls longtext ,\
                            primary key (words)
                            )"""
    cursor.execute(sql)
    # 从download_apk中读取review
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
    db.close()
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
            insert_words(words)
        # print("!!!!!!!!!!!!!!!!!", y)
        y += 1
        if y % 500 == 0:
            print("目前文章数：",y)
    print("第一次遍历分词结束")
    # f = open(r'index_review.txt', 'a')
    #
    # f.write('\n'.join(insert_w))
    #
    # f.close()
