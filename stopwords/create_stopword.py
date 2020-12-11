import sys

# 中文停用词表	cn_stopwords.txt
# 哈工大停用词表	hit_stopwords.txt
# 百度停用词表	baidu_stopwords.txt
# 四川大学机器智能实验室停用词库	scu_stopwords.txt
baidu_stop = [line.strip() for line in open('baidu_stopwords.txt', 'r', encoding='UTF-8').readlines()]
cn_stop = [line.strip() for line in open('cn_stopwords.txt', 'r', encoding='UTF-8').readlines()]
hit_stop = [line.strip() for line in open('hit_stopwords.txt', 'r', encoding='UTF-8').readlines()]
scu_stop = [line.strip() for line in open('scu_stopwords.txt', 'r', encoding='UTF-8').readlines()]

stopwords = []

for words in baidu_stop:
    if words not in stopwords:
        stopwords.append(words)

for words in cn_stop:
    if words not in stopwords:
        stopwords.append(words)

for words in hit_stop:
    if words not in stopwords:
        stopwords.append(words)

for words in scu_stop:
    if words not in stopwords:
        stopwords.append(words)
# print(stopwords)
f = open(r'./stopwords.txt', 'a')

f.write('\n'.join(stopwords))

f.close()
