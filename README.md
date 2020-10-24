# Coolapk_search
SDU《信息检索》课程设计，Cooapk应用列表爬取+索引构建+搜索引擎查询练习程序

|Author|Collapsar-G|
|---|---
|E-mail|collapsar@gmail.xiheye.club|

## 1 要求
以下是检索的基本要求：可以利用lucene、nutch等开源工具，利用Python、Java等编程语言，但需要分别演示并说明原理。
* 1. __Web网页信息抽取__
以Coolapk官网为起点进行遍历爬取，保持爬虫在  https://www.coolapk.com/apk/  之内（即只爬取这个站点的网页），爬取的网页数量越多越好。

* 2. __索引构建__
对上一步爬取到的网页进行结构化预处理，包括基于模板的信息抽取、分字段解析、分词、构建索引等。

* 3. __检索排序__
对上一步构建的索引库进行查询，对于给定的查询，给出检索结果，明白排序的原理及方法。

## 2 运行方式


## 3 所需python库
* scrapy
* requests
* pymongo
* whoosh
* jieba
* flask

## 4 所需数据库
* MySQL
* Navicat Premium 15 可视化工具（可选）

## 5 爬虫特性