import pymysql
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import requests
import simplejson

from search.relevancy import rele
from sqlalchemy.orm import class_mapper
from flask_bootstrap import Bootstrap

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r"/*")
# connect MySQL
db = pymysql.connect("localhost", "root", "8520", "coolapk")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
bootstrap = Bootstrap(app)  # 为应用初始化 bootstrap


def as_dict(obj):
    # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    # 上面的有缺陷，表字段和属性不一致会有问题
    return dict((col.name, getattr(obj, col.name)) \
                for col in class_mapper(obj.__class__).mapped_table.c)


def tojson(result):
    review = result[0][10]
    if review == '0':
            review = '暂无点评'
    return {
        'id': result[0][0],
        'imgurl': result[0][1],
        'downloadurl': result[0][2],
        'skipurl': "https:/www.coolapk.com/apk/" + result[0][3],
        'name': result[0][4],
        'version': result[0][5],
        'downloadcount': result[0][6],
        'focus_count': result[0][7],
        'commentcount': result[0][8],
        'language': result[0][9],
        'review': review,
        'score': result[0][13],
        'categorylabels': result[0][14]
    }


@app.route('/index/')
def index():
    if request.method == 'GET':
        return render_template('base.html')


@app.route('/search/<index>')
def search(index):
    # index = request.form.get('index')
    print(index)

    reles = rele(index)
    context = {}
    data = []
    for i in range(0, 30):
        # context[i + 1] = reles[i]
        try:
            sql = """select * from download_apk where skip_url = '{}'""".format(reles[i][0])
            cursor.execute(sql)
            result = cursor.fetchall()
            # data = tojson(result)

            data.append(tojson(result))
            # json.dumps(data, ensure_ascii=False)
            # context = {i: data}
            # print(result)
            # 提交到数据库执行
            db.commit()
            # print(result)
        except:
            print("找不到这个app")
            # print(words[0], word)
            # db.close()
            # 如果发生错误则回滚
            # exit(0)
        # json.dumps(context)
    # print(data)

    # print( type(data))
    return simplejson.dumps(data, ensure_ascii=False)
    # # return render_template('detail.html')
    # print(index)
    # return u'index'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8090)
